from django.contrib import admin
from expenses.models import Receipt,Expense
from ocr.models import OCRExtractedData
from users.models import CustomUser

# Register models from the expenses app
admin.site.register(Receipt)

# Register models from the ocr app
admin.site.register(OCRExtractedData)

admin.site.register(CustomUser)

admin.site.register(Expense)