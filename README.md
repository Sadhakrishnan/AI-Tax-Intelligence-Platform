# AI Tax Intelligence Platform

A comprehensive backend API designed for automated financial document processing, intelligent tax estimation, and anomaly detection. It features a Retrieval-Augmented Generation (RAG) chat assistant to provide interactive insights on tax and financial queries, along with robust endpoints for extracting structured data from various document formats.

## Features

- **Document Ingestion & Extraction**: Upload financial documents (PDF, JPG, PNG, CSV) and extract structured data automatically.
- **Tax Estimation**: Retrieve educational tax estimates based on extracted data.
- **Anomaly Detection**: Flag anomalies and potential fraud in financial documents.
- **RAG Chat Assistant**: Ask tax and financial questions and get context-aware answers powered by a Retrieval-Augmented Generation system.
- **Agentic Workflows**: Includes specialized agents for OCR, summarization, and tax calculations.

## Tech Stack

- **Backend**: FastAPI
- **Language**: Python
- **Key Modules**:
  - `ocr.py`: Optical Character Recognition processing
  - `classifier.py`: Document classification
  - `parser.py`: Parsing structured text
  - `dashboard.py`: Interactive user interface (e.g., Streamlit)
  - Specialized components organized in `agents/`, `rag/`, `extraction/`, and `reports/` directories.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tax
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On macOS/Linux: source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have your `requirements.txt` populated with the necessary packages like `fastapi`, `uvicorn`, etc.)*

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API documentation:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints Overview

- `POST /upload`: Upload financial documents.
- `POST /extract`: Trigger structured data extraction using a document ID.
- `GET /tax_estimate`: Retrieve educational tax estimates.
- `GET /anomalies`: Retrieve detected anomalies and fraud flags.
- `POST /chat`: Interact with the RAG-based chat endpoint for tax questions.

## Disclaimer

This project provides *educational tax estimates only* and should not be considered professional financial or legal advice.
