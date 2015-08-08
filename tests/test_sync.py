"""
.. module:: dj-stripe.tests.test_sync
   :synopsis: dj-stripe Sync Method Tests.

.. moduleauthor:: Alex Kavanaugh (@kavdev)

"""

import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.testcases import TestCase

from mock import patch, PropertyMock
from stripe.error import StripeError, InvalidRequestError

from djstripe.models import Customer
from djstripe.sync import sync_subscriber, sync_plans


class TestSyncSubscriber(TestCase):
    fake_stripe_customer = "test_stripe_customer"

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",
                                                         email="test@example.com",
                                                         password="123")

    @patch("djstripe.models.Customer.sync_charges")
    @patch("djstripe.models.Customer.sync_invoices")
    @patch("djstripe.models.Customer.sync_current_subscription")
    @patch("djstripe.models.Customer.sync")
    @patch("djstripe.models.Customer.stripe_customer", new_callable=PropertyMock, return_value=fake_stripe_customer)
    @patch("stripe.Customer.create", return_value=PropertyMock(id="cus_xxx1234567890"))
    def test_sync_success(self, stripe_customer_create_mock, stripe_customer_mock,
                          sync_mock, sync_current_subscription_mock, sync_invoices_mock,
                          sync_charges_mock):

        sync_subscriber(self.user)
        self.assertEqual(1, Customer.objects.count())
        self.assertEqual(self.fake_stripe_customer, Customer.objects.get(subscriber=self.user).stripe_customer)

        sync_mock.assert_called_once_with()
        sync_current_subscription_mock.assert_called_once_with()
        sync_invoices_mock.assert_called_once_with()
        sync_charges_mock.assert_called_once_with()

    @patch("djstripe.models.Customer.sync")
    @patch("djstripe.models.Customer.stripe_customer", new_callable=PropertyMock, return_value="test_stripe_customer")
    @patch("stripe.Customer.create", return_value=PropertyMock(id="cus_xxx1234567890"))
    def test_sync_fail(self, stripe_customer_create_mock, stripe_customer_mock, sync_mock):
        sync_mock.side_effect = InvalidRequestError("No such customer:", "blah")

        sync_subscriber(self.user)

        self.assertEqual("ERROR: No such customer:", sys.stdout.getvalue().strip())


class TestSyncPlans(TestCase):

    @patch("stripe.Plan.create")
    def test_plan_created(self, plan_create_mock):
        sync_plans()
        self.assertTrue("Plan created for test", sys.stdout.getvalue().strip())

        plan_create_mock.assert_any_call(api_key=settings.STRIPE_SECRET_KEY,
                                        amount=1000,
                                        interval="month",
                                        name="Test Plan 0",
                                        currency="usd",
                                        id="test_id_0")

        plan_create_mock.assert_any_call(api_key=settings.STRIPE_SECRET_KEY,
                                        amount=2500,
                                        interval="month",
                                        name="Test Plan 1",
                                        currency="usd",
                                        id="test_id")

        plan_create_mock.assert_any_call(api_key=settings.STRIPE_SECRET_KEY,
                                        amount=5000,
                                        interval="month",
                                        name="Test Plan 2",
                                        currency="usd",
                                        id="test_id_2")

        plan_create_mock.assert_any_call(api_key=settings.STRIPE_SECRET_KEY,
                                        amount=5000,
                                        interval="month",
                                        name="Test Plan 3",
                                        currency="usd",
                                        id="test_id_3")

        plan_create_mock.assert_any_call(api_key=settings.STRIPE_SECRET_KEY,
                                        amount=7000,
                                        interval="month",
                                        name="Test Plan 4",
                                        currency="usd",
                                        id="test_id_4",
                                        trial_period_days=7)

        self.assertEqual(5, plan_create_mock.call_count)

    @patch("stripe.Plan.create")
    def test_plan_exists(self, plan_create_mock):
        plan_create_mock.side_effect = StripeError("Plan already exists.")

        sync_plans()
        self.assertTrue("ERROR: Plan already exists.", sys.stdout.getvalue().strip())
