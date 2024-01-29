from paymentgateway.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--1z+hzm52694_0jg3817t!)9$nz$f^z&0vowq!@6#q#e(1(skw"

WSGI_APPLICATION = "paymentgateway.wsgi.application"

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

CORALPAY_INVOKEPAYMENT_URL = "https://testdev.coralpay.com:5000/GwApi/api/v1/InvokePayment/"
CORALPAY_TRANSACTIONQUERY_URL = "https://testdev.coralpay.com:5000/GwApi/api/v1/TransactionQuery/"
CORALPAY_INVOKE_USSD_URL = "https://testdev.coralpay.com/cgateproxy/api/invokereference"

# CORALPAY_RETURN_URL = "https://google.com"
CORALPAY_RETURN_URL = "http://127.0.0.1:8000/gateway/api/v0/payment-status/"
CORALPAY_CALLBACKURL_SUCCESS = "http://127.0.0.1:8000/gateway/api/v0/success/"
CORALPAY_WEBSOCKETURL_SUCCESS = "http://127.0.0.1:8000/ws/success/"
CORALPAY_CALLBACKURL_FAILURE = "http://127.0.0.1:8000/gateway/api/v0/failure/"
CORALPAY_WEBSOCKETURL_FAILURE = "http://127.0.0.1:8000/ws/failure/"
CORALPAY_TRACEID = "9900990285"
CORALPAY_TERMINALID = "40016857947"
CORALPAY_PRODUCTID = "aa12443d"
CORALPAY_MERCHANT_USERNAME = "ojapaXIgaPqMJdRVh%I*NXppJGV)*mo"
CORALPAY_MERCHANT_PASSWORD = "83Y36$47@P^0TTME@NV?*5MFY8H5I?E8N95#I940"
CORALPAY_MERCHANTID = "4001686OJGUHK01"
CORALPAY_KEY = "59d7b52c-758e-4060-8bc3-cdffd780fb2f"
CORALPAY_TOKEN = "eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTUxMiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2YWNhY2EzYS04YzlmLTQyYTgtYjYzNy01NThkODQyZWU2M2YiLCJNZXJjaGFudElkIjoiNDAwMTY4Nk9KR1VISzAxIiwiZXhwIjoxNzI2MzMwNzQ3LCJpc3MiOiJodHRwczovL2NvcmFscGF5LmNvbSIsImF1ZCI6Imh0dHBzOi8vY29yYWxwYXkuY29tIn0.xrAqFg18m9u_j5TMrHEfOA0djU8Wnndh6ojOCHv3mmjdQOI6yuM0gYsyjaLQeQZbCpe5CMNmMTo7uQR249udFw"

# PAY WITH CARD DETAILS
CORALPAY_REQUESTPAYMENTWITHCARD_URL = "https://cnptest.coralpay.com:9443/octoweb/cnp/requestPayment/"
CORALPAY_CARD_MERCHANTID = "3051OJP10000001"
CORALPAY_PAYWITHCARD_TOKEN = "KHR0IyNtQDAkQG1hdm0lKCUxJSRAMCo1ZiU0dihqM25AOmFlMjEzYjNmOThkYTE5YjdlN2VlNzkwNjZlYTczODc3MGY0NDQ5MzgzOGE4NTc2OTJhZjYzNDU4MjY0MjEzNzVkMmVmMjM0NTAwNjBlOWM3YWZlZjVhN2RkZjYzOWZlY2EyZmU3MjdkM2IwZjRiNTYwNDgxOTU4NjM3NmVmM2NjMjcxMTAzNDI5N2Q1ZjNlZGJkMWY1ZjM4ZGIwY2Q3MzY5MDNjNmYwOGViNjM1YTQ5Njc2NzAwNmI="

# PAY WITH DYNAMIC BANK TRANSFER
CORALPAY_CLIENTID = "4001459DHEKNS17"
CORALPAY_DYNAMIC_PAYWITHTRANSFER_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/dynamicAccount/"
CORALPAY_DPWT_USERNAME = "Ojaypay_User"

# PAY WITH STATIC BANK TRANSFER
CORALPAY_STATIC_PAYWITHTRANSFER_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/staticAccount/"

# PAY WITH TRANSFER REQUERY
CORALPAY_PAYWITHTRANSFER_REQUERY_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/getTransactionDetails/"
CORALPAY_CLIENT_PASSWORD = "77LO!T38TY8I##@M09G$&TKKBX?JV"

# FETCH ACCOUNT TRANSACTIONS
CORALPAY_FETCH_ACCOUNT_TRANSACTIONS_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/partners/getAccountTransactions/"

# FETCH PARTNER TRANSACTIONS
CORALPAY_FETCH_PARTNER_TRANSACTIONS_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/partners/fetch-partner-transactions"


# TRANSACTION PAYMENT NOTIFICATION
CORALPAY_MERCHANT_ACCOUNT_NUMBER = "7003268673"
CORALPAY_MERCHANT_PAYMENT_NOTIFICATION_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/testPartnerRequest/"

# GET BANK LIST 
CORALPAY_GET_BANK_LIST_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/moneytransfer/apis/listOfBanks/"

# PAY DIRECT URL
CORALPAY_PAYDIRECT_URL = "http://sandbox1.coralpay.com:8080/paywithtransfer/v1/directpaywithaccount/apis/onetimepayment/"