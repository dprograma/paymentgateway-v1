from typing import Any
import json
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime
import requests
import hashlib
import time
import random
import base64


@method_decorator(csrf_exempt, name="dispatch")
class InvokePayment(APIView):
    authentication_classes = []
    permission_classes = []

    def generate_random_number(self, length=10) -> str:
        lower_bound = 10 ** (length - 1)
        upper_bound = 10**length - 1
        randomnumber = str(random.randint(lower_bound, upper_bound)) + str(
            int(time.time())
        )
        return randomnumber

    def generate_unix_time_seconds(self) -> str:
        current_timestamp = str(int(time.time()))
        return current_timestamp

    def generate_sha256(self) -> tuple[str, str, str]:
        merchantId = settings.CORALPAY_MERCHANTID
        traceId = self.generate_random_number()
        current_timestamp = self.generate_unix_time_seconds()
        key = settings.CORALPAY_KEY
        signature_string = f"{merchantId}{traceId}{current_timestamp}{key}"
        signature = hashlib.sha256(signature_string.encode("utf-8")).hexdigest()
        return traceId, current_timestamp, signature

    def process_payment(
        self, request, traceId, timeStamp, signature, merchantId
    ) -> tuple[bool, Any] | tuple[bool, str]:
        email = request.data.get("email")
        name = request.data.get("name")
        title = request.data.get("title")
        amount = request.data.get("amount")
        phone = request.data.get("phone")  # or however you obtain it
        token_user_id = phone  # assuming phone number serves as user token ID

        payload = json.dumps(
            {
                "requestHeader": {
                    "merchantId": merchantId,
                    "timeStamp": timeStamp,
                    "signature": signature,
                },
                "customer": {
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "tokenUserId": token_user_id,
                },
                "customization": {
                    "logoUrl": "https://images.app.goo.gl/A19dJZCBxZbewZFm9",
                    "title": title,
                    "description": "Service Payment",
                },
                "metaData": {
                    "data1": "sample data",
                    "data2": "another sample data",
                    "data3": "sample info",
                },
                "traceId": traceId,
                "productId": settings.CORALPAY_PRODUCTID,
                "amount": amount,
                "currency": "NGN",
                "feeBearer": "M",
                "returnUrl": settings.CORALPAY_RETURN_URL,
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.CORALPAY_TOKEN}",
        }

        response = requests.post(
            settings.CORALPAY_INVOKEPAYMENT_URL, headers=headers, data=payload
        )

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.text

    def post(self, request, *args, **kwargs) -> Response:
        traceId, current_timestamp, signature = self.generate_sha256()

        is_successful, invoke_data = self.process_payment(
            request, traceId, current_timestamp, signature, settings.CORALPAY_MERCHANTID
        )

        if is_successful:
            return Response(
                {
                    "status": "success",
                    "invoke_data": invoke_data,
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {
                    "status": "failed",
                    "message": "InvokePayment failed",
                    "invoke_data": invoke_data,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class PaymentStatus(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs) -> Response:
        all_data = {}

        # For GET parameters
        all_data["GET"] = request.GET.dict()

        return Response(
            {"status": "success", "data": all_data}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs) -> Response:
        all_data = {}

        # For POST parameters
        all_data["POST"] = request.POST.dict()

        return Response(
            {"status": "success", "data": all_data}, status=status.HTTP_200_OK
        )


@method_decorator(csrf_exempt, name="dispatch")
class RequestPaymentWithCard(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        amount = request.data.get("amount")
        merchant_ref = generate_random_string(25)
        payload = json.dumps(
            {
                "merchantId": settings.CORALPAY_CARD_MERCHANTID,
                "merchantRef": merchant_ref,
                "amount": amount,
                "callBackUrlSuccess": settings.CORALPAY_CALLBACKURL_SUCCESS,
                "callBackUrlFailed": settings.CORALPAY_CALLBACKURL_FAILURE,
                "isTokenize": 0,
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {settings.CORALPAY_PAYWITHCARD_TOKEN}",
        }

        try:
            response = requests.post(
                settings.CORALPAY_REQUESTPAYMENTWITHCARD_URL,
                headers=headers,
                data=payload,
            )

            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {
                    "status": "request failed",
                    "error": "Error processing payment request.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SuccessUrl(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        all_data = {}

        # For POST parameters
        all_data["POST"] = request.POST.dict()

        channel_layer = get_channel_layer()
        print("DEFAULT CHANNEL LAYER: ", channel_layer)

        async_to_sync(channel_layer.group_send)(
            "payment_status",
            {"type": "send_payment_status", "message": "Payment Successful or Failure"},
        )

        return Response(
            {"status": "success", "data": all_data}, status=status.HTTP_200_OK
        )


@method_decorator(csrf_exempt, name="dispatch")
class FailureUrl(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        all_data = {}

        # For POST parameters
        all_data["POST"] = request.POST.dict()

        channel_layer = get_channel_layer()

        # Trigger message sent to WebSocket
        async_to_sync(channel_layer.group_send)(
            "your_group_name",
            {"type": "send_payment_status", "message": "Payment Successful or Failure"},
        )

        return Response(
            {"status": "failed", "data": all_data}, status=status.HTTP_200_OK
        )


@method_decorator(csrf_exempt, name="dispatch")
class RequestPaymentWithTransfer(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        # Generate a unique reference number
        reference_no = generate_unique_reference()
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        amount = request.data.get("amount")
        customer_name = f"{firstname} {lastname}"
        username = settings.CORALPAY_DPWT_USERNAME

        # Combine username and reference_no
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")
        reqUrl = settings.CORALPAY_DYNAMIC_PAYWITHTRANSFER_URL

        headersList = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_value}",
        }

        payload = json.dumps(
            {
                "requestHeader": {
                    "clientId": settings.CORALPAY_CLIENTID,
                    "requestType": "Bank Transfer",
                },
                "customerName": customer_name,
                "referenceNumber": reference_no,
                "transactionAmount": amount,
            }
        )

        try:
            response = requests.post(reqUrl, data=payload, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class RequestPaymentWithTransferStatic(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        # Combine username and reference_no
        reference_no = generate_unique_reference()
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")
        amount = request.data.get("amount")
        customer_name = f"{firstname} {lastname}"
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")

        reqUrl = settings.CORALPAY_STATIC_PAYWITHTRANSFER_URL

        headersList = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_value}",
        }

        payload = json.dumps(
            {
                "requestHeader": {
                    "clientId": settings.CORALPAY_CLIENTID,
                    "requestType": "Bank Transfer",
                },
                "customerName": customer_name,
                "referenceNumber": reference_no,
                "customerID ": "Microwave",
            }
        )

        try:
            response = requests.post(reqUrl, data=payload, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class GetTransactionDetails(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs) -> Response:
        # Combine username and reference_no
        reference_no = generate_unique_reference()
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")

        reqUrl = settings.CORALPAY_PAYWITHTRANSFER_REQUERY_URL

        headersList = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_value}",
        }

        payload = json.dumps(
            {
                "requestHeader": {
                    "clientId": settings.CORALPAY_CLIENTID,
                    "requestType": "Bank Transfer",
                },
                "referenceNumber": reference_no,
            }
        )

        try:
            response = requests.post(reqUrl, data=payload, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class FetchAccountTransactions(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs) -> Response:
        customer_account_number = request.data.get("account_no")
        from_date = request.data.get("from_date")
        to_date = request.data.get("to_date")
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{customer_account_number}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")
        reqUrl = f"{settings.CORALPAY_FETCH_ACCOUNT_TRANSACTIONS_URL}?accountNumber={customer_account_number}&fromDate={from_date}&toDate={to_date}"

        headersList = {"Authorization": f"Basic {encoded_value}"}

        try:
            response = requests.get(reqUrl, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class FetchPartnerTransactions(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        client_id = settings.CORALPAY_CLIENTID
        from_date = request.data.get("from_date")
        to_date = request.data.get("to_date")
        username = settings.CORALPAY_DPWT_USERNAME
        password = settings.CORALPAY_CLIENT_PASSWORD

        # Basic auth
        encoded_value = encode_base64(f"{username}:{password}")

        reqUrl = f"{settings.CORALPAY_FETCH_PARTNER_TRANSACTIONS_URL}?clientId={client_id}&fromDate={from_date}&toDate={to_date}"

        headersList = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_value}" 
        }

        try:
            response = requests.get(reqUrl, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

@method_decorator(csrf_exempt, name="dispatch")
class TransactionPaymentNotification(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        merchant_account_number = settings.CORALPAY_MERCHANT_ACCOUNT_NUMBER
        source_account_number = request.data.get('source-account-number')
        source_account_name = request.data.get('source-account-name')
        transaction_amount = request.data.get('amount')
        transaction_date = datetime.now().strftime("%DD-%MM-%YYYY %H:%M:%S")
        
        reference_no = generate_unique_reference()
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")
        reqUrl = settings.CORALPAY_MERCHANT_PAYMENT_NOTIFICATION_URL

        headersList = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_value}" 
        }

        payload = json.dumps({
            "account_number": merchant_account_number,
            "source_account_number": source_account_number,
            "source_account_name": source_account_name,
            "transaction_amount": transaction_amount,
            "source_bank_code": "N/A",
            "source_bank_name": "N/A",
            "tran_date_time": transaction_date,
            "service_charge": 50,
            "referenceNumber":reference_no,
            "account_name": "Ojapay",
            "currency": "NGN",
            "operationReference": "8fb-8b5e-41d8-bb54-a6bff38ba82f",
            "module_value": "3161b3628d23605f50f1db10a5001b3f68d9eecb35c3fa6d5fdaa97c8b08a1954b27b40553f4c9f3ae4f18d4e6accfe4f46201d2124152b79a3eced04149efdc"
        })

        
        try:
            response = requests.post(reqUrl, data=payload,  headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )   
            
            
@method_decorator(csrf_exempt, name="dispatch")
class GetBankList(APIView): 
    authentication_classes = []
    permission_classes = []        

    def get(self, request, *args, **kwargs):
        reference_no = generate_unique_reference()
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")
        reqUrl = settings.CORALPAY_GET_BANK_LIST_URL

        headersList = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_value}" 
        }

        try:
            response = requests.get(reqUrl, headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )  
        

@method_decorator(csrf_exempt, name="dispatch")
class DirectPay(APIView): 
    authentication_classes = []
    permission_classes = []  
    
    def post(self, request, *args, **kwargs):
        client_id = settings.CORALPAY_CLIENTID
        firstname = request.data.get('firstname')
        lastname = request.data.get('lastname')
        amount = request.data.get('amount')
        customer_name = f"{firstname} {lastname}"
        reference_no = generate_unique_reference()
        username = settings.CORALPAY_DPWT_USERNAME
        combined_string = f"{reference_no}:{username}"

        # Hash the combined string using SHA-512 and get it in hexadecimal form
        hashed_value = hash_sha512(combined_string)

        # Basic auth
        encoded_value = encode_base64(f"{username}:{hashed_value}")
        reqUrl = settings.CORALPAY_PAYDIRECT_URL

        headersList = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_value}" 
        }

        payload = json.dumps({
            "requestHeader": {
                "clientId": client_id,
                "requestType": "Bank Transfer"   
            },
            "customerName": customer_name,
            "referenceNumber": reference_no,
            "transactionAmount": amount
        })       

        try:
            response = requests.post(reqUrl, data=payload,  headers=headersList)
            if response.status_code == 200:
                return Response(
                    {"status": "request successful", "data": response.json()},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"status": "request failed", "error": response.text},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except requests.exceptions.RequestException:
            return Response(
                {"status": "request failed", "error": response.text},
                status=status.HTTP_400_BAD_REQUEST,
            )  
        
            
    
def generate_random_string(length=25) -> str:
    current_timestamp = str(int(time.time()))

    hex_length = length - len(current_timestamp)

    hex_string = "".join(random.choice("0123456789ABCDEF") for _ in range(hex_length))

    return hex_string + current_timestamp


def generate_unique_reference(length=13) -> str:
    current_timestamp = str(int(time.time()))

    hex_length = length - len(current_timestamp)

    if hex_length > 0:
        hex_string = "".join(random.choice("0123456789") for _ in range(hex_length))
    else:
        hex_string = ""

    return hex_string + current_timestamp


def hash_sha512(text_to_hash) -> str:
    # Create a new sha512 hash object
    hash_object = hashlib.sha512()
    # Update the hash object with the bytes of the string
    hash_object.update(text_to_hash.encode())
    # Get the hexadecimal representation of the digest
    hash_hex = hash_object.hexdigest()
    return hash_hex


def encode_base64(data) -> str:
    # Encode the data using Base64 encoding
    return base64.b64encode(data.encode("utf-8")).decode("utf-8")
