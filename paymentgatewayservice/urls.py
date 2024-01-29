from django.urls import path
from .views import (
    DirectPay,
    GetBankList,
    InvokePayment,
    PaymentStatus,
    RequestPaymentWithCard,
    SuccessUrl,
    FailureUrl,
    RequestPaymentWithTransfer,
    RequestPaymentWithTransferStatic,
    GetTransactionDetails,
    FetchAccountTransactions,
    FetchPartnerTransactions,
    TransactionPaymentNotification,
)

urlpatterns = [
    path("invokepayment/", InvokePayment.as_view(), name="invoke_payment"),
    # http://127.0.0.1:8000/gateway/api/v0/invokepayment
    path("payment-status/", PaymentStatus.as_view(), name="payment_status"),
    # http://127.0.0.1:8000/gateway/api/v0/payment-status
    path("paywithcard/", RequestPaymentWithCard.as_view(), name="pay_with_card"),
    # http://127.0.0.1:8000/gateway/api/v0/paywithcard
    path("success/", SuccessUrl.as_view(), name="success"),
    path("failure/", FailureUrl.as_view(), name="failure"),
    path(
        "paywithtransfer",
        RequestPaymentWithTransfer.as_view(),
        name="dynamic_pay_with_transfer",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/paywithtransfer
    path(
        "static-paywithtransfer/",
        RequestPaymentWithTransferStatic.as_view(),
        name="static_pay_with_transfer",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/static-paywithtransfer
    path(
        "get-transaction-details/",
        GetTransactionDetails.as_view(),
        name="get_transaction_details",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/get-transaction-details
    path(
        "fetch-account-transactions/",
        FetchAccountTransactions.as_view(),
        name="fetch_account_transaction",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/fetch-account-transactions
    path(
        "fetch-partner-transactions/",
        FetchPartnerTransactions.as_view(),
        name="fetch_partner_transaction",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/fetch-partner-transactions
    path(
        "merchant-transactions-notification/",
        TransactionPaymentNotification.as_view(),
        name="merchanttransactions_notification",
    ),
    # http://127.0.0.1:8000/gateway/api/v0/merchant-transactions-notification
    path("get-bank-list/", GetBankList.as_view(), name="get_bank_list"),
    # http://127.0.0.1:8000/gateway/api/v0/get-bank-list
    path("direct-pay/", DirectPay.as_view(), name="direct_pay"),
    # http://127.0.0.1:8000/gateway/api/v0/direct-pay
]
