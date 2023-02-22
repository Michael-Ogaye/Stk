from django import forms
from django.contrib.auth.forms import UserCreationForm
from c_auth.models import CustomUser




class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','phone_number')

class SignInForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=('email','password1')

class PurchasForm(forms.Form):
    phone=forms.IntegerField()