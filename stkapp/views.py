from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from .models import LNM
from .serializers import LNMSerializer


class LNMCallbackUrlAPIView(CreateAPIView):
    queryset = LNM.objects.all()
    serializer_class = LNMSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        

        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
    
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
            "Value"
        ]
    
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][1]["Value"]
        

        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][3]["Value"]
    

        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
            4
        ]["Value"]
        

        from datetime import datetime

        str_transaction_date = str(transaction_date)
        

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
        print(transaction_datetime, "this should be an transaction_datetime")

        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
        


        from .models import LNM

        l_model = LNM.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            Balance=balance,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )

        l_model.save()

        from rest_framework.response import Response

        return Response({"Transaction succesful"})