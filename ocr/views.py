from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import OCRExtractedData
from expenses.models import Receipt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ocr_data_list(request):
    ocr_items = OCRExtractedData.objects.select_related("receipt").filter(receipt__user=request.user)

    data = []
    for item in ocr_items:
        data.append({
            "id": item.id,
            "receipt": item.receipt.id,
            "raw_text": item.raw_text,
            "extracted_amount": str(item.extracted_amount) if item.extracted_amount else None,
            "extracted_date": item.extracted_date,
            "extracted_merchant": item.extracted_merchant,
            "processed_at": item.processed_at,
        })

    return Response(data)
