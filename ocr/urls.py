from django.urls import path
from .views import ocr_data_list

urlpatterns = [
    path('ocr_data/', ocr_data_list, name='ocr-data-list'),
]
