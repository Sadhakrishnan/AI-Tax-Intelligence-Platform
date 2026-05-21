import cv2
import numpy as np
import pytesseract
from PIL import Image
import os

# Set Tesseract path if necessary (Windows example)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRPipeline:
    """
    Robust OCR pipeline with image preprocessing using OpenCV.
    """

    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def preprocess_image(self, pil_image):
        """
        Applies preprocessing to improve OCR accuracy.
        1. Grayscale
        2. Denoising
        3. Thresholding (Adaptive)
        4. Skew correction (placeholder)
        """
        # Convert PIL to OpenCV format
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        if len(open_cv_image.shape) == 3:
            open_cv_image = open_cv_image[:, :, ::-1].copy()
        
        # 1. Grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # 2. Denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # 3. Thresholding
        thresh = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh

    def extract_text(self, pil_image):
        """
        Extracts text from a PIL image using Tesseract.
        """
        # Preprocess
        processed_img = self.preprocess_image(pil_image)
        
        # OCR
        text = pytesseract.image_to_string(processed_img)
        
        # Data (confidence, bounding boxes)
        data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT)
        
        # Calculate mean confidence
        confidences = [int(c) for c in data['conf'] if c != '-1']
        mean_conf = np.mean(confidences) if confidences else 0
        
        return {
            "text": text,
            "confidence": mean_conf,
            "data": data  # Detailed results if needed
        }

if __name__ == "__main__":
    # Test block
    print("OCR Pipeline initialized.")
