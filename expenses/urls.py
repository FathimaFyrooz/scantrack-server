from django.urls import path
from .views import upload_receipt,get_expenses,add_expense

urlpatterns = [
    path("upload/", upload_receipt, name="upload_receipt"),
    path("get_expenses/",get_expenses,name="get_expenses"),
    path("add_expense/",add_expense,name="add_expense"),
]
