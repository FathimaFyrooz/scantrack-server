from django.urls import path
from .views import upload_receipt,get_expenses

urlpatterns = [
    path("upload/", upload_receipt, name="upload_receipt"),
    path("get_expenses/",get_expenses,name="get_expenses"),
]
