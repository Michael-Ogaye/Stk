from django.urls import path
from .views import LNMCallbackUrlAPIView,product,products,purchase

urlpatterns = [
    path('lnm/',LNMCallbackUrlAPIView.as_view(), name='lnm' ),
    path('',products,name='prods'),
    path('prod/<int:pk>',product,name='prod'),
    path('purchase/<int:pk',purchase,name='purch')
]
