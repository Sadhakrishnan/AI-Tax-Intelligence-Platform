import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.ocr_agent import OCRAgent
from agents.tax_agent import TaxAgent
from agents.summary_agent import SummaryAgent
from rag.tax_knowledge import TaxKnowledgeSystem
from extraction.invoice_extractor import InvoiceExtractor

# Page Config
st.set_page_config(page_title="AI Tax Intelligence Platform", layout="wide", page_icon="📊")

# Initialize Agents & Systems
@st.cache_resource
def init_systems():
    return {
        "ocr": OCRAgent(),
        "tax": TaxAgent(),
        "summary": SummaryAgent(),
        "rag": TaxKnowledgeSystem(),
        "extractor": InvoiceExtractor()
    }

systems = init_systems()
systems["rag"].initialize_knowledge_base()

# Sidebar
st.sidebar.title("💎 TaxAI Copilot")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Document Upload", "Tax Knowledge (RAG)", "Reports"])

# --- Dashboard ---
if menu == "Dashboard":
    st.header("📊 Financial Intelligence Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Expenses", "₹45,200", "+12%")
    col2.metric("Estimated Deductions", "₹8,400", "+5%")
    col3.metric("Tax Liability", "₹2,100", "-2%")
    col4.metric("Compliance Score", "94%", "+2%")

    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Spending by Category")
        df = pd.DataFrame({
            "Category": ["Travel", "Food", "Software", "Utilities", "Office"],
            "Amount": [12000, 4500, 15000, 3200, 10500]
        })
        fig = px.pie(df, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Monthly Trend")
        df_trend = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "Expenses": [35000, 42000, 38000, 45200, 29000]
        })
        fig_line = px.line(df_trend, x="Month", y="Expenses", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

# --- Document Upload ---
elif menu == "Document Upload":
    st.header("📂 Document Ingestion")
    
    uploaded_file = st.file_uploader("Upload Receipt or Invoice (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file:
        # Save temp file
        temp_path = os.path.join("data", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Agents working..."):
            # 1. OCR
            raw_text = systems["ocr"].process(temp_path)
            
            # 2. Extract (Using a mock prompt/response for demo)
            # In real usage: response = llm.call(systems["extractor"].generate_prompt(raw_text))
            # Here we mock a response for the UI flow
            mock_json = '{"vendor_name": "Amazon India", "total_amount": 4500.0, "currency": "INR", "date": "2024-05-10", "tax_amount": 810.0, "gst_number": "27AAACA1234F1Z5"}'
            extracted_data = systems["extractor"].parse_llm_response(mock_json)
            
            # 3. Tax Analysis
            analysis = systems["tax"].analyze_invoice(extracted_data)
            
            # 4. Summary
            insights = systems["summary"].generate_summary({**extracted_data.dict(), **analysis})

        st.success("Processing Complete!")
        
        tab1, tab2, tab3 = st.tabs(["📄 OCR Result", "🔍 Structured Data", "💡 AI Insights"])
        
        with tab1:
            st.text_area("Raw Text Extracted", raw_text, height=300)
            
        with tab2:
            st.json(extracted_data.dict())
            
        with tab3:
            st.info(insights["summary"])
            st.write(insights["insight"])
            
            if analysis["compliance_flags"]:
                st.warning("Compliance Flags Detected:")
                for flag in analysis["compliance_flags"]:
                    st.write(f"- {flag}")
            else:
                st.success("No compliance issues detected.")

# --- RAG Knowledge ---
elif menu == "Tax Knowledge (RAG)":
    st.header("🧠 Tax Knowledge Assistant")
    st.write("Ask questions about tax rules, deductions, and policies.")
    
    query = st.text_input("Enter your question:", placeholder="Can I deduct my home office equipment?")
    
    if query:
        with st.spinner("Searching knowledge base..."):
            result = systems["rag"].answer_question(query)
            st.markdown(f"### Answer\n{result['answer']}")
            if result['sources']:
                st.markdown("**Sources:** " + ", ".join(result['sources']))

# --- Reports ---
elif menu == "Reports":
    st.header("📄 Report Generation")
    st.write("Generate and download your financial tax report.")
    
    if st.button("Generate PDF Report"):
        st.success("Report generated successfully! (Mock)")
        st.download_button("Download Report", data=b"Mock PDF Content", file_name="Tax_Report.pdf")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | Powered by Agentic AI")
