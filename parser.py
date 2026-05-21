import fitz  # PyMuPDF
import pdfplumber
import os
from PIL import Image
import io

class DocumentParser:
    """
    Handles ingestion of various document formats (PDF, JPG, PNG).
    """

    @staticmethod
    def pdf_to_images(pdf_path, output_dir=None):
        """
        Converts PDF pages to a list of PIL Images.
        """
        images = []
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Scale up for better OCR
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
            
            if output_dir:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                img.save(os.path.join(output_dir, f"page_{page_num}.png"))
        
        return images

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extracts digital text directly from PDF if available.
        """
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    @staticmethod
    def load_image(image_path):
        """
        Loads an image file into a PIL Image object.
        """
        return Image.open(image_path)

if __name__ == "__main__":
    # Test block
    print("Document Parser initialized.")
