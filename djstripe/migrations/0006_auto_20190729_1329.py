# Generated by Django 2.2.3 on 2019-07-29 13:29

import django.db.models.deletion
from django.db import migrations, models

import djstripe.enums
import djstripe.fields


def fix_djstripepaymentmethod_index_name_forwards(apps, schema_editor):
    # Altering the index is required because while we changed the name of old PaymentMethod model to
    # DjStripePaymentMethod, the migrations didn't update the names of index.
    # In the current migration, we create a new PaymentMethod model, hence before creating it, its
    # better to rename the old index.
    if not schema_editor.connection.vendor.startswith("postgres"):
        return
    schema_editor.execute(
        "ALTER INDEX djstripe_paymentmethod_id_0b9251df_like rename TO djstripe_paymentmethod_legacy_id_0b9251df_like"
    )


def fix_djstripepaymentmethod_index_name_backwards(apps, schema_editor):
    if not schema_editor.connection.vendor.startswith("postgres"):
        return
    schema_editor.execute(
        "ALTER INDEX djstripe_paymentmethod_legacy_id_0b9251df_like rename TO djstripe_paymentmethod_id_0b9251df_like"
    )


class Migration(migrations.Migration):

    dependencies = [("djstripe", "0005_auto_20190710_1023")]

    operations = [
        # Altering the index is required because while we chnage the name of old PaymentMethod model to
        # DjStripePaymentMethod, the migrations didn't update the names of index.
        # In the current migration, we create a new PaymentMethod model, hence before creating it, its
        # better to rename the old index.
        migrations.RunPython(
            fix_djstripepaymentmethod_index_name_forwards,
            fix_djstripepaymentmethod_index_name_backwards,
        ),
        migrations.CreateModel(
            name="PaymentIntent",
            fields=[
                (
                    "djstripe_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("id", djstripe.fields.StripeIdField(max_length=255, unique=True)),
                (
                    "livemode",
                    models.NullBooleanField(
                        default=None,
                        help_text="Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.",
                    ),
                ),
                (
                    "created",
                    djstripe.fields.StripeDateTimeField(
                        blank=True,
                        help_text="The datetime this object was created in stripe.",
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.",
                        null=True,
                    ),
                ),
                ("djstripe_created", models.DateTimeField(auto_now_add=True)),
                ("djstripe_updated", models.DateTimeField(auto_now=True)),
                (
                    "amount",
                    djstripe.fields.StripeQuantumCurrencyAmountField(
                        help_text="Amount intended to be collected by this PaymentIntent."
                    ),
                ),
                (
                    "amount_capturable",
                    djstripe.fields.StripeQuantumCurrencyAmountField(
                        help_text="Amount that can be captured from this PaymentIntent."
                    ),
                ),
                (
                    "amount_received",
                    djstripe.fields.StripeQuantumCurrencyAmountField(
                        help_text="Amount that was collected by this PaymentIntent."
                    ),
                ),
                (
                    "canceled_at",
                    djstripe.fields.StripeDateTimeField(
                        default=None,
                        help_text="Populated when status is canceled, this is the time at which the PaymentIntent was canceled. Measured in seconds since the Unix epoch.",
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "cancellation_reason",
                    models.CharField(
                        help_text="User-given reason for cancellation of this PaymentIntent, one of duplicate, fraudulent, requested_by_customer, or failed_invoice.",
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "capture_method",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.CaptureMethod,
                        help_text="Capture method of this PaymentIntent, one of automatic or manual.",
                        max_length=9,
                    ),
                ),
                (
                    "client_secret",
                    models.CharField(
                        help_text="The client secret of this PaymentIntent. Used for client-side retrieval using a publishable key.",
                        max_length=255,
                    ),
                ),
                (
                    "confirmation_method",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.ConfirmationMethod,
                        help_text="Confirmation method of this PaymentIntent, one of manual or automatic.",
                        max_length=9,
                    ),
                ),
                (
                    "currency",
                    djstripe.fields.StripeCurrencyCodeField(
                        help_text="Three-letter ISO currency code", max_length=3
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default="",
                        help_text="An arbitrary string attached to the object. Often useful for displaying to users.",
                    ),
                ),
                (
                    "last_payment_error",
                    djstripe.fields.JSONField(
                        help_text="The payment error encountered in the previous PaymentIntent confirmation."
                    ),
                ),
                (
                    "next_action",
                    djstripe.fields.JSONField(
                        help_text="If present, this property tells you what actions you need to take in order for your customer to fulfill a payment using the provided source."
                    ),
                ),
                (
                    "payment_method_types",
                    djstripe.fields.JSONField(
                        help_text="The list of payment method types (e.g. card) that this PaymentIntent is allowed to use."
                    ),
                ),
                (
                    "receipt_email",
                    models.CharField(
                        help_text="Email address that the receipt for the resulting payment will be sent to.",
                        max_length=255,
                    ),
                ),
                (
                    "setup_future_usage",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.IntentUsage,
                        help_text="Indicates that you intend to make future payments with this PaymentIntent’s payment method. If present, the payment method used with this PaymentIntent can be attached to a Customer, even after the transaction completes. Use `on_session` if you intend to only reuse the payment method when your customer is present in your checkout flow. Use `off_session` if your customer may or may not be in your checkout flow. Stripe uses `setup_future_usage` to dynamically optimize your payment flow and comply with regional legislation and network rules. For example, if your customer is impacted by SCA, using `off_session` will ensure that they are authenticated while processing this PaymentIntent. You will then be able to make later off-session payments for this customer.",
                        max_length=11,
                    ),
                ),
                (
                    "shipping",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="Shipping information for this PaymentIntent.",
                        null=True,
                    ),
                ),
                (
                    "statement_descriptor",
                    models.CharField(
                        blank=True,
                        help_text="Extra information about a PaymentIntent. This will appear on your customer’s statement when this PaymentIntent succeeds in creating a charge.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "status",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.PaymentIntentStatus,
                        help_text="Status of this PaymentIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, requires_capture, canceled, or succeeded. You can read more about PaymentIntent statuses here.",
                        max_length=16,
                    ),
                ),
                (
                    "transfer_data",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="The data with which to automatically create a Transfer when the payment is finalized. See the PaymentIntents Connect usage guide for details.",
                        null=True,
                    ),
                ),
                (
                    "transfer_group",
                    models.CharField(
                        help_text="A string that identifies the resulting payment as part of a group. See the PaymentIntents Connect usage guide for details.",
                        blank=True,
                        max_length=255,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        help_text="Customer this PaymentIntent is for if one exists.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.Customer",
                    ),
                ),
                (
                    "on_behalf_of",
                    models.ForeignKey(
                        help_text="The account (if any) for which the funds of the PaymentIntent are intended.",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djstripe.Account",
                    ),
                ),
            ],
            options={"get_latest_by": "created", "abstract": False},
        ),
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "djstripe_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("id", djstripe.fields.StripeIdField(max_length=255, unique=True)),
                (
                    "livemode",
                    models.NullBooleanField(
                        default=None,
                        help_text="Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.",
                    ),
                ),
                (
                    "created",
                    djstripe.fields.StripeDateTimeField(
                        blank=True,
                        help_text="The datetime this object was created in stripe.",
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.",
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="A description of this object.", null=True
                    ),
                ),
                ("djstripe_created", models.DateTimeField(auto_now_add=True)),
                ("djstripe_updated", models.DateTimeField(auto_now=True)),
                (
                    "billing_details",
                    djstripe.fields.JSONField(
                        help_text="Billing information associated with the PaymentMethod that may be used or required by particular types of payment methods."
                    ),
                ),
                (
                    "card",
                    djstripe.fields.JSONField(
                        help_text="If this is a card PaymentMethod, this hash contains details about the card."
                    ),
                ),
                (
                    "card_present",
                    djstripe.fields.JSONField(
                        help_text="If this is an card_present PaymentMethod, this hash contains details about the Card Present payment method."
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        help_text="The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        help_text="Customer to which this PaymentMethod is saved.This will not be set when the PaymentMethod has not been saved to a Customer.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment_methods",
                        to="djstripe.Customer",
                    ),
                ),
            ],
            options={"get_latest_by": "created", "abstract": False},
        ),
        migrations.AlterField(
            model_name="payout",
            name="destination",
            field=models.ForeignKey(
                help_text="Bank account or card the payout was sent to.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="djstripe.BankAccount",
            ),
        ),
        migrations.CreateModel(
            name="SetupIntent",
            fields=[
                (
                    "djstripe_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("id", djstripe.fields.StripeIdField(max_length=255, unique=True)),
                (
                    "livemode",
                    models.NullBooleanField(
                        default=None,
                        help_text="Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.",
                    ),
                ),
                (
                    "created",
                    djstripe.fields.StripeDateTimeField(
                        blank=True,
                        help_text="The datetime this object was created in stripe.",
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.",
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="A description of this object.", null=True
                    ),
                ),
                ("djstripe_created", models.DateTimeField(auto_now_add=True)),
                ("djstripe_updated", models.DateTimeField(auto_now=True)),
                (
                    "application",
                    models.CharField(
                        blank=True,
                        help_text="ID of the Connect application that created the SetupIntent.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "cancellation_reason",
                    models.CharField(
                        help_text="Reason for cancellation of this SetupIntent, one of abandoned, requested_by_customer, or duplicate",
                        max_length=255,
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    "client_secret",
                    models.CharField(
                        blank=True,
                        help_text="The client secret of this SetupIntent. Used for client-side retrieval using a publishable key.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "last_setup_error",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="The error encountered in the previous SetupIntent confirmation.",
                        null=True,
                    ),
                ),
                (
                    "next_action",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="If present, this property tells you what actions you need to take inorder for your customer to continue payment setup.",
                        null=True,
                    ),
                ),
                (
                    "payment_method_types",
                    djstripe.fields.JSONField(
                        help_text="The list of payment method types (e.g. card) that this PaymentIntent is allowed to use."
                    ),
                ),
                (
                    "status",
                    djstripe.fields.StripeEnumField(
                        enum=djstripe.enums.SetupIntentStatus,
                        help_text="Status of this SetupIntent, one of requires_payment_method, requires_confirmation, requires_action, processing, canceled, or succeeded.",
                        max_length=9,
                    ),
                ),
                (
                    "usage",
                    djstripe.fields.StripeEnumField(
                        default="off_session",
                        enum=djstripe.enums.IntentUsage,
                        help_text="Indicates how the payment method is intended to be used in the future.",
                        max_length=11,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        help_text="Customer this SetupIntent belongs to, if one exists.",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.Customer",
                    ),
                ),
                (
                    "on_behalf_of",
                    models.ForeignKey(
                        help_text="The account (if any) for which the setup is intended.",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.Account",
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        help_text="Payment method used in this PaymentIntent.",
                        null=True,
                        blank=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.PaymentMethod",
                    ),
                ),
            ],
            options={"get_latest_by": "created", "abstract": False},
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "djstripe_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("id", djstripe.fields.StripeIdField(max_length=255, unique=True)),
                (
                    "livemode",
                    models.NullBooleanField(
                        default=None,
                        help_text="Null here indicates that the livemode status is unknown or was previously unrecorded. Otherwise, this field indicates whether this record comes from Stripe test mode or live mode operation.",
                    ),
                ),
                (
                    "created",
                    djstripe.fields.StripeDateTimeField(
                        blank=True,
                        help_text="The datetime this object was created in stripe.",
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="A set of key/value pairs that you can attach to an object. It can be useful for storing additional information about an object in a structured format.",
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="A description of this object.", null=True
                    ),
                ),
                ("djstripe_created", models.DateTimeField(auto_now_add=True)),
                ("djstripe_updated", models.DateTimeField(auto_now=True)),
                (
                    "biling_address_collection",
                    models.CharField(
                        blank=True,
                        help_text="The value (auto or required) for whether Checkoutcollected the customer’s billing address.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "cancel_url",
                    models.CharField(
                        blank=True,
                        help_text="The URL the customer will be directed to if theydecide to cancel payment and return to your website.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "client_reference_id",
                    models.CharField(
                        blank=True,
                        help_text="A unique string to reference the Checkout Session.This can be a customer ID, a cart ID, or similar, andcan be used to reconcile the session with your internal systems.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "customer_email",
                    models.CharField(
                        blank=True,
                        help_text="If provided, this value will be used when the Customer object is created.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "display_items",
                    djstripe.fields.JSONField(
                        blank=True,
                        help_text="The line items, plans, or SKUs purchased by the customer.",
                        null=True,
                    ),
                ),
                (
                    "locale",
                    models.CharField(
                        blank=True,
                        help_text="The IETF language tag of the locale Checkout is displayed in.If blank or auto, the browser’s locale is used.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "payment_method_types",
                    djstripe.fields.JSONField(
                        help_text="The list of payment method types (e.g. card) that this Checkout Session is allowed to accept."
                    ),
                ),
                (
                    "submit_type",
                    djstripe.fields.StripeEnumField(
                        blank=True,
                        enum=djstripe.enums.SubmitTypeStatus,
                        help_text="Describes the type of transaction being performed by Checkoutin order to customize relevant text on the page, such as the submit button.",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "success_url",
                    models.CharField(
                        blank=True,
                        help_text="The URL the customer will be directed to after the payment or subscriptioncreation is successful.",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        help_text="Customer this Checkout is for if one exists.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.Customer",
                    ),
                ),
                (
                    "payment_intent",
                    models.ForeignKey(
                        help_text="PaymentIntent created if SKUs or line items were provided.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.PaymentIntent",
                    ),
                ),
                (
                    "subscription",
                    models.ForeignKey(
                        help_text="Subscription created if one or more plans were provided.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djstripe.Subscription",
                    ),
                ),
            ],
            options={"get_latest_by": "created", "abstract": False},
        ),
        migrations.AddField(
            model_name="paymentintent",
            name="payment_method",
            field=models.ForeignKey(
                help_text="Payment method used in this PaymentIntent.",
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="djstripe.PaymentMethod",
            ),
        ),
        migrations.AddField(
            model_name="charge",
            name="payment_intent",
            field=models.ForeignKey(
                help_text="PaymentIntent associated with this charge, if one exists.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="charges",
                to="djstripe.PaymentIntent",
            ),
        ),
        migrations.AddField(
            model_name="invoice",
            name="payment_intent",
            field=models.OneToOneField(
                help_text="The PaymentIntent associated with this invoice. The PaymentIntent is generated when the invoice is finalized, and can then be used to pay the invoice.Note that voiding an invoice will cancel the PaymentIntent",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="djstripe.PaymentIntent",
            ),
        ),
        migrations.AddField(
            model_name="subscription",
            name="pending_setup_intent",
            field=models.ForeignKey(
                blank=True,
                help_text="We can use this SetupIntent to collect user authentication when creating a subscription without immediate payment or updating a subscription’s payment method, allowing you to optimize for off-session payments.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="setup_intents",
                to="djstripe.SetupIntent",
            ),
        ),
    ]
