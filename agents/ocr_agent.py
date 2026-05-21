from ingestion.parser import DocumentParser
from ingestion.ocr import OCRPipeline

class OCRAgent:
    """
    Agent responsible for converting documents into raw text.
    """
    def __init__(self):
        self.parser = DocumentParser()
        self.ocr_pipeline = OCRPipeline()

    def process(self, file_path: str):
        print(f"[OCR Agent] Processing {file_path}")
        ext = file_path.split('.')[-1].lower()
        
        full_text = ""
        if ext == 'pdf':
            # Try direct extraction first
            full_text = self.parser.extract_text_from_pdf(file_path)
            if not full_text.strip():
                # Fallback to OCR
                images = self.parser.pdf_to_images(file_path)
                for img in images:
                    result = self.ocr_pipeline.extract_text(img)
                    full_text += result['text'] + "\n"
        elif ext in ['jpg', 'jpeg', 'png']:
            img = self.parser.load_image(file_path)
            result = self.ocr_pipeline.extract_text(img)
            full_text = result['text']
            
        return full_text

if __name__ == "__main__":
    agent = OCRAgent()
    print("OCR Agent ready.")
