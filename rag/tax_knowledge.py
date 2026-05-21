from rag.vector_store import TaxVectorStore
from langchain.docstore.document import Document

class TaxKnowledgeSystem:
    """
    Retrieval-Augmented Generation (RAG) system for tax-related queries.
    """

    def __init__(self):
        self.vector_store = TaxVectorStore()
        # Initial knowledge base (can be expanded)
        self.default_rules = [
            Document(page_content="Business travel expenses including flights and hotels are generally tax-deductible if incurred for business purposes.", metadata={"source": "Internal Policy"}),
            Document(page_content="Office equipment like laptops and monitors can be claimed as capital expenditure with depreciation benefits.", metadata={"source": "Tax Guidelines"}),
            Document(page_content="GST/VAT numbers are mandatory on all invoices exceeding 200 INR for valid tax credit claims.", metadata={"source": "Compliance Rules"}),
        ]

    def initialize_knowledge_base(self):
        """
        Seeds the vector store with default tax rules if empty.
        """
        if not self.vector_store.load_index():
            print("Initializing new knowledge base...")
            self.vector_store.create_index(self.default_rules)

    def answer_question(self, query: str) -> dict:
        """
        Retrieves relevant context and generates an answer (placeholder for LLM).
        """
        relevant_docs = self.vector_store.search(query)
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        # In a real implementation, we would pass context + query to an LLM.
        # For now, we return the retrieved context as a "grounded" answer.
        
        answer = f"Based on our records: {context}" if context else "I couldn't find specific information on that topic."
        
        return {
            "answer": answer,
            "sources": [doc.metadata.get("source", "Unknown") for doc in relevant_docs]
        }

if __name__ == "__main__":
    tks = TaxKnowledgeSystem()
    tks.initialize_knowledge_base()
    result = tks.answer_question("Can I deduct travel expenses?")
    print(result)
