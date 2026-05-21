from extraction.invoice_extractor import ExtractedInvoice
from categorization.classifier import ExpenseClassifier

class TaxAgent:
    """
    Agent responsible for tax calculations, deductions, and compliance flags.
    """
    def __init__(self):
        self.classifier = ExpenseClassifier()

    def analyze_invoice(self, invoice: ExtractedInvoice):
        print(f"[Tax Agent] Analyzing invoice from {invoice.vendor_name}")
        
        # 1. Categorize
        category = self.classifier.get_category(invoice.vendor_name)
        
        # 2. Check Deductibility (Rule-based for now)
        is_deductible = False
        deduction_reason = ""
        if category in ["Travel", "Office Supplies", "Software & Subscriptions", "Marketing"]:
            is_deductible = True
            deduction_reason = f"Category '{category}' is typically a deductible business expense."
        
        # 3. Compliance Check
        compliance_flags = []
        if not invoice.gst_number:
            compliance_flags.append("Missing GST/VAT ID on invoice.")
        if invoice.total_amount <= 0:
            compliance_flags.append("Zero or negative total amount detected.")

        return {
            "category": category,
            "is_deductible": is_deductible,
            "deduction_reason": deduction_reason,
            "compliance_flags": compliance_flags,
            "estimated_tax_impact": invoice.tax_amount if is_deductible else 0
        }

if __name__ == "__main__":
    agent = TaxAgent()
    print("Tax Agent ready.")
