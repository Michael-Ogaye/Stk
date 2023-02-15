from django.db import models

# Create your models here.



class LNM(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    ResultCode = models.IntegerField(blank=True, null=True)
    ResultDesc = models.CharField(max_length=120, blank=True, null=True)
    Amount = models.FloatField(blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    Balance = models.CharField(max_length=12, blank=True, null=True)
    TransactionDate = models.DateTimeField(blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return f"{self.PhoneNumber}   {self.Amount}  {self.MpesaReceiptNumber}"

class Product(models.Model):
    name=models.CharField(max_length=16)
    description=models.CharField(max_length=355)
    price=models.IntegerField()
    def __str__(self):
        return 'f{self.name}'

class Profile(models.Model):
    phone=models.IntegerField()


