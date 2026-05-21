from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

class TaxReportGenerator:
    """
    Generates professional PDF tax and financial reports.
    """

    def generate(self, data: dict, output_path: str = None):
        """
        Creates a PDF report from the provided data.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer if not output_path else output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Financial Tax Intelligence Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Summary Paragraph
        summary_text = f"This report provides a summary of financial documents processed. Total expenses analyzed: {data.get('total_expenses', 'N/A')}. Estimated tax impact: {data.get('tax_impact', 'N/A')}."
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 24))

        # Expense Table
        elements.append(Paragraph("Expense Breakdown", styles['Heading2']))
        table_data = [["Category", "Amount", "Deductible"]]
        for item in data.get("expenses", []):
            table_data.append([item['category'], f"INR {item['amount']}", "Yes" if item['is_deductible'] else "No"])

        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))

        # Compliance Flags
        if data.get("compliance_flags"):
            elements.append(Paragraph("Compliance Alerts", styles['Heading2']))
            for flag in data["compliance_flags"]:
                elements.append(Paragraph(f"• {flag}", styles['Normal']))

        # Build PDF
        doc.build(elements)
        
        if not output_path:
            return buffer.getvalue()

if __name__ == "__main__":
    # Test block
    gen = TaxReportGenerator()
    test_data = {
        "total_expenses": "45,200",
        "tax_impact": "8,400",
        "expenses": [
            {"category": "Travel", "amount": 12000, "is_deductible": True},
            {"category": "Software", "amount": 15000, "is_deductible": True},
            {"category": "Food", "amount": 4500, "is_deductible": False}
        ],
        "compliance_flags": ["Missing GST ID on 2 invoices"]
    }
    gen.generate(test_data, "test_report.pdf")
    print("Report generated: test_report.pdf")
