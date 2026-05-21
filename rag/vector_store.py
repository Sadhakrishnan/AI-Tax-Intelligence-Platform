from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os

class TaxVectorStore:
    """
    Manages the vector database for RAG.
    """

    def __init__(self, index_path="data/faiss_index"):
        self.index_path = index_path
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def create_index(self, documents: list[Document]):
        """
        Creates a new FAISS index from a list of LangChain Documents.
        """
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        self.vector_store = FAISS.from_documents(docs, self.embeddings)
        self.save_index()

    def save_index(self):
        """
        Saves the FAISS index to local storage.
        """
        if self.vector_store:
            self.vector_store.save_local(self.index_path)

    def load_index(self):
        """
        Loads the FAISS index from local storage.
        """
        if os.path.exists(self.index_path):
            self.vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            return True
        return False

    def search(self, query: str, k=3):
        """
        Performs a similarity search in the vector store.
        """
        if not self.vector_store:
            if not self.load_index():
                return []
        
        return self.vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    # Test block
    print("Tax Vector Store initialized.")
