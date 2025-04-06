import json
from openai import OpenAI
from django.conf import settings

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def parse_receipt_data(raw_text):
    """
    Use OpenAI Chat Completions to parse receipt data and extract amount, date, and merchant.
    Returns a dictionary with keys "extracted_amount", "extracted_date", and "extracted_merchant".
    """
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Extract the following details from the receipt text below:\n"
                        "- Extracted Amount in USD (as a decimal number, e.g., 123.45)\n"
                        "- Extracted Date (in YYYY-MM-DD format)\n"
                        "- Extracted Merchant (as text)\n"
                        "Return ONLY a valid JSON object with exactly these keys: \"extracted_amount\", \"extracted_date\", \"extracted_merchant\".\n"
                        "Do not include any additional text or commentary."
                    )
                },
                {
                    "type": "text",
                    "text": f"Receipt text: \"{raw_text}\""
                }
            ]
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Replace with your desired model if needed
            messages=messages,
        )
        result_text = response.choices[0].message.content.strip()
        print(result_text)
        if not result_text:
            raise ValueError("Empty response from OpenAI")
        data = json.loads(result_text)
        return data
    except Exception as e:
        print("Error parsing receipt data with OpenAI:", e)
        # Return default values if parsing fails
        return {
            "extracted_amount": None,
            "extracted_date": None,
            "extracted_merchant": None,
        }
