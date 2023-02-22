from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from .models import LNM,Product
from .serializers import LNMSerializer
from .stkpush import StkPush
from .forms import SignupForm,SignInForm,PurchasForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('prods')
    else:
        form = SignupForm()
    return render(request, 'stkapp/signup.html', {'form': form})

def signin(request):
    if request.method=='POST':
        form=SignInForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user=authenticate(email,password)
            if user is not None:
                login(request,user)
    else:
        form = SignInForm()
    return render(request, 'stkapp/signin.html', {'form': form})




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


@login_required(login_url='login')
def products(request):
    all_products=Product.objects.all()
    return render(request,'stkapp/products.html',{'prods':all_products})

@login_required(login_url='login')
def product(request,pk):
    a_prod=Product.objects.get(pk=pk)
    return render(request,'stkapp/product.html',{'prod':a_prod})

@login_required(login_url='login')
def purchase(request,pk):
    if request.method=='POST':
        form=PurchasForm(request.POST)
        if form.is_valid():
            a_prod=Product.objects.get(pk=pk)
            price=a_prod.price
            phone=form.cleaned_data.get('phone')
            used_no=int(str(phone)[::-1][0:10][::-1] +'254')
            
            StkPush().lNM(price,used_no)
            return redirect('prods')
    
    else:
        form =PurchasForm()
    return render(request, 'stkapp/purch.html', {'form': form})



        
