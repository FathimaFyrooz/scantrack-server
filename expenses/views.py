import os
import uuid
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.files.storage import default_storage
from expenses.models import Receipt,Expense
from ocr.models import OCRExtractedData
from django.views.decorators.csrf import csrf_exempt
from .openai import parse_receipt_data

import pdfplumber

def perform_pdf_ocr(file_path):
    print("perform ocr function called")
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    text = ""
    try:
        with pdfplumber.open(full_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        text = f"Error processing PDF: {str(e)}"
    return text.strip()

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_receipt(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("receipt")
            print("file is:", file)
            user = request.user
            print("user is authenticated:", user)

            if not file:
                return JsonResponse({"error": "No file uploaded"}, status=400)

            file_extension = file.name.split(".")[-1].lower()
            if file_extension != "pdf":
                return JsonResponse({"error": "Only PDF receipts are supported in this phase."}, status=400)

            unique_filename = f"receipt_{uuid.uuid4().hex}.{file_extension}"
            print("filename is:", unique_filename)

            file_path = os.path.join("receipts", unique_filename)
            print("filepath is:", file_path)

            saved_path = default_storage.save(file_path, file)

            receipt = Receipt.objects.create(
                user=user,
                file_path=saved_path,
                uploaded_at=now(),
                status="pending",
            )
            print("Receipt created:", receipt)

            raw_text = perform_pdf_ocr(saved_path)
            print("Extracted text:", raw_text)
            
            if not raw_text:
                raw_text = "No text extracted from the PDF."

            parsed_data = parse_receipt_data(raw_text)
            extracted_amount = parsed_data.get("extracted_amount")
            extracted_date = parsed_data.get("extracted_date")
            extracted_merchant = parsed_data.get("extracted_merchant")
            print("Parsed data:", parsed_data)

            try:
                ocr_data = OCRExtractedData.objects.create(
                    receipt=receipt,
                    raw_text=raw_text,
                    extracted_amount=extracted_amount,
                    extracted_date=extracted_date,
                    extracted_merchant=extracted_merchant,
                )
                print("OCR Data created:", ocr_data)
            except Exception as ocr_e:
                print("Error creating OCRExtractedData record:", str(ocr_e))
                receipt.status = "failed"
                receipt.save()
                return JsonResponse({"error": "OCR data creation failed: " + str(ocr_e)}, status=500)

            receipt.status = "processed"
            receipt.save()

            return JsonResponse(
                {"message": "File uploaded and processed successfully", "receipt_id": receipt.id},
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def get_expenses(request):
    if request.method == 'GET':
        expenses = Expense.objects.all()
        data = [
            {
                'id': expense.id,
                'amount': float(expense.amount),
                'date': expense.date.strftime('%Y-%m-%d'),
                'merchant': expense.merchant,
                'notes': expense.notes,
                'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for expense in expenses
        ]
        return JsonResponse(data, safe=False)