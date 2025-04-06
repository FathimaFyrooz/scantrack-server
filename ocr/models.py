from django.db import models
from expenses.models import Receipt  # Import Receipt model from expenses app

class OCRExtractedData(models.Model):
    receipt = models.OneToOneField(Receipt, on_delete=models.CASCADE, related_name="ocr_data")
    raw_text = models.TextField()
    extracted_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extracted_date = models.DateField(null=True, blank=True)
    extracted_merchant = models.CharField(max_length=255, null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCR Data for Receipt {self.receipt.id}"
