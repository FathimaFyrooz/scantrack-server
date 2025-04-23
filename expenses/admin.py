from django.contrib import admin
from expenses.models import Receipt,Expense
from ocr.models import OCRExtractedData
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Custom admin for Receipt
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file_path', 'uploaded_at', 'status')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('user__username', 'status')
    ordering = ('-uploaded_at',)

# Custom admin for Expense
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receipt', 'amount', 'date', 'merchant', 'created_at')
    list_filter = ('date', 'merchant')
    search_fields = ('user__username', 'merchant', 'notes')
    ordering = ('-date',)
class OCRExtractedDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'receipt',
        'extracted_amount',
        'extracted_date',
        'extracted_merchant',
        'processed_at',
    )
    search_fields = ('receipt__id', 'extracted_merchant')
    list_filter = ('processed_at', 'extracted_merchant')
    ordering = ('-processed_at',)

admin.site.register(OCRExtractedData, OCRExtractedDataAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Expense, ExpenseAdmin)