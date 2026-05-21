class SummaryAgent:
    """
    Agent responsible for generating financial summaries and insights.
    """
    def generate_summary(self, data: dict):
        vendor = data.get("vendor_name", "Unknown")
        total = data.get("total_amount", 0)
        category = data.get("category", "Uncategorized")
        is_deductible = data.get("is_deductible", False)
        
        summary = f"Processed a {total} INR transaction from {vendor}."
        insight = f"This expense was categorized as {category}."
        if is_deductible:
            insight += " It is likely tax-deductible, which could help reduce your taxable income."
        else:
            insight += " This category is usually not deductible for business purposes."
            
        return {
            "summary": summary,
            "insight": insight
        }

if __name__ == "__main__":
    agent = SummaryAgent()
    print("Summary Agent ready.")
