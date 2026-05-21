from pydantic import BaseModel, Field
from typing import List, Optional
import json

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = 1.0
    unit_price: Optional[float] = 0.0
    amount: float

class ExtractedInvoice(BaseModel):
    vendor_name: str = Field(..., description="Name of the merchant or vendor")
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    subtotal: Optional[float] = 0.0
    tax_amount: Optional[float] = 0.0
    total_amount: float
    currency: str = "INR"
    gst_number: Optional[str] = None
    line_items: List[LineItem] = []

class InvoiceExtractor:
    """
    Handles structured data extraction from OCR text using LLMs.
    """

    def __init__(self, model_provider="gemini"):
        self.model_provider = model_provider

    def generate_prompt(self, ocr_text: str):
        """
        Creates a prompt for the LLM to extract structured data.
        """
        schema = ExtractedInvoice.schema_json()
        prompt = f"""
        Extract structured financial information from the following OCR text of an invoice/receipt.
        
        OCR Text:
        ---
        {ocr_text}
        ---
        
        Return the result as a valid JSON object matching this schema:
        {schema}
        
        Rules:
        - If a field is missing, use null or a reasonable default.
        - Ensure total_amount is accurate.
        - Identify line items if possible.
        """
        return prompt

    def parse_llm_response(self, response_text: str) -> ExtractedInvoice:
        """
        Parses JSON response from LLM into a Pydantic model.
        """
        try:
            # Basic cleanup of LLM response (handling markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(response_text)
            return ExtractedInvoice(**data)
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            # Return a minimal valid object as fallback
            return ExtractedInvoice(vendor_name="Unknown", total_amount=0.0)

if __name__ == "__main__":
    # Test block
    print("Invoice Extractor initialized.")
