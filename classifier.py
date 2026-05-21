from typing import Dict, List

class ExpenseClassifier:
    """
    Categorizes expenses into standard tax/business categories.
    """
    
    CATEGORIES = [
        "Travel", "Food & Dining", "Utilities", "Healthcare", 
        "Office Supplies", "Software & Subscriptions", "Entertainment", 
        "Marketing", "Legal & Professional", "Other Business Expense"
    ]

    KEYWORD_MAP = {
        "uber": "Travel",
        "ola": "Travel",
        "amazon": "Office Supplies",
        "swiggy": "Food & Dining",
        "zomato": "Food & Dining",
        "microsoft": "Software & Subscriptions",
        "google": "Software & Subscriptions",
        "aws": "Software & Subscriptions",
        "airtel": "Utilities",
        "jio": "Utilities",
    }

    def classify_by_keyword(self, vendor_name: str) -> str:
        """
        Quick keyword-based classification.
        """
        vendor_lower = vendor_name.lower()
        for keyword, category in self.KEYWORD_MAP.items():
            if keyword in vendor_lower:
                return category
        return "Other Business Expense"

    def classify_semantic(self, description: str) -> str:
        """
        Placeholder for semantic classification using Sentence Transformers or LLM.
        """
        # In a real implementation, this would use a cross-encoder or LLM call.
        return "Other Business Expense"

    def get_category(self, vendor_name: str, description: str = "") -> str:
        """
        Main entry point for classification.
        """
        # 1. Try keyword mapping
        category = self.classify_by_keyword(vendor_name)
        
        # 2. If default, try semantic (placeholder)
        if category == "Other Business Expense" and description:
            # category = self.classify_semantic(description)
            pass
            
        return category

if __name__ == "__main__":
    classifier = ExpenseClassifier()
    print(classifier.get_category("Uber Technologies"))
