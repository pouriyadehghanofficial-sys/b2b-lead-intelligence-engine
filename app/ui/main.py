"""Streamlit UI for B2B Lead Intelligence Engine"""

import streamlit as st
import pandas as pd
from datetime import datetime
import logging
import os
from pathlib import Path

from app.core.pipeline import LeadDiscoveryPipeline
from app.core.checkpoint import CheckpointManager
from app.export.excel_export import ExcelExporter
from app.export.json_export import JSONExporter
from app.export.csv_export import CSVExporter
from app.config.settings import get_settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page config
st.set_page_config(
    page_title="B2B Lead Intelligence Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state initialization
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'leads' not in st.session_state:
    st.session_state.leads = []
if 'checkpoint_manager' not in st.session_state:
    st.session_state.checkpoint_manager = CheckpointManager()


def main():
    """Main UI function"""
    st.title("🔍 B2B Lead Intelligence Engine")
    st.markdown("*Find and validate Iranian B2B leads from public sources*")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys
        st.subheader("Search Providers")
        tavily_key = st.text_input(
            "Tavily API Key",
            type="password",
            value=os.getenv("TAVILY_API_KEY", ""),
            help="Optional - for enhanced search"
        )
        
        exa_key = st.text_input(
            "Exa API Key",
            type="password",
            value=os.getenv("EXA_API_KEY", ""),
            help="Optional - for semantic search"
        )
        
        st.subheader("LLM Providers")
        openrouter_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=os.getenv("OPENROUTER_API_KEY", ""),
            help="Optional - for AI query generation"
        )
        
        # Set environment variables
        if tavily_key:
            os.environ["TAVILY_API_KEY"] = tavily_key
        if exa_key:
            os.environ["EXA_API_KEY"] = exa_key
        if openrouter_key:
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
        
        st.divider()
        st.subheader("Advanced Settings")
        max_queries = st.slider("Max Search Queries", 5, 50, 20)
        batch_size = st.slider("Batch Size", 5, 50, 10)
        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.5, 0.1
        )
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Search Parameters")
        
        col_industry, col_location = st.columns(2)
        with col_industry:
            industry = st.text_input(
                "Industry/Sector",
                placeholder="e.g., کاشی و سرامیک (Tile & Ceramic)",
                help="Persian or English"
            )
        
        with col_location:
            location = st.text_input(
                "Province/City",
                placeholder="e.g., یزد (Yazd)",
                help="Persian or English"
            )
        
        col_product, col_quantity = st.columns(2)
        with col_product:
            product = st.text_input(
                "Product/Solution (Optional)",
                placeholder="e.g., سیستم هوش مصنوعی",
            )
        
        with col_quantity:
            quantity = st.number_input(
                "Target Lead Count",
                min_value=10,
                max_value=5000,
                value=100,
                step=50,
            )
        
        target_roles = st.multiselect(
            "Target Roles",
            [
                "مدیرعامل (CEO)",
                "مدیر فروش (Sales Manager)",
                "مدیر بازرگانی (Commercial Manager)",
                "مسئول خرید (Purchase Officer)",
                "مدیر تولید (Production Manager)",
                "مدیر کیفیت (Quality Manager)",
            ],
            default=["مدیر فروش (Sales Manager)", "مسئول خرید (Purchase Officer)"],
        )
    
    with col2:
        st.header("ℹ️ Info")
        st.info(
            """**How it works:**
            
            1. 🔍 Generate smart search queries
            2. 📡 Search multiple providers
            3. 🏢 Extract companies & contacts
            4. 📱 Find phone numbers
            5. 🔗 Match people to roles
            6. ⭐ Score and rank leads
            7. 📊 Export results
            """
        )
    
    # Action buttons
    st.divider()
    col_action1, col_action2, col_action3 = st.columns([1, 1, 2])
    
    with col_action1:
        if st.button("🚀 Start Search", use_container_width=True):
            if not industry or not location:
                st.error("Please enter Industry and Location")
            else:
                run_pipeline(
                    industry=industry,
                    location=location,
                    product=product,
                    target_roles=target_roles,
                    quantity=quantity,
                    max_queries=max_queries,
                )
    
    with col_action2:
        if st.button("📂 Resume", use_container_width=True):
            st.info("Resume functionality coming soon...")
    
    with col_action3:
        if st.session_state.leads:
            st.success(f"✅ Found {len(st.session_state.leads)} leads")
    
    # Results section
    if st.session_state.leads:
        st.divider()
        display_results(st.session_state.leads, confidence_threshold)


def run_pipeline(
    industry: str,
    location: str,
    product: str = None,
    target_roles: list = None,
    quantity: int = 100,
    max_queries: int = 20,
):
    """Run the lead discovery pipeline"""
    with st.spinner("🔄 Initializing pipeline..."):
        pipeline = LeadDiscoveryPipeline()
        st.session_state.pipeline = pipeline
    
    with st.spinner("🔍 Discovering leads..."):
        try:
            leads = pipeline.discover(
                industry=industry,
                location=location,
                product=product,
                target_roles=target_roles,
                quantity=quantity,
                max_queries=max_queries,
            )
            
            st.session_state.leads = leads
            st.success(f"✅ Found {len(leads)} qualified leads!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Pipeline failed: {str(e)}")
            logger.error(f"Pipeline error: {str(e)}", exc_info=True)


def display_results(leads: list, confidence_threshold: float = 0.5):
    """Display search results"""
    # Statistics
    st.header("📊 Results")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    verified = len([l for l in leads if l.status.value == 'VERIFIED'])
    likely = len([l for l in leads if l.status.value == 'LIKELY'])
    possible = len([l for l in leads if l.status.value == 'POSSIBLE'])
    
    with col1:
        st.metric("Total Leads", len(leads))
    with col2:
        st.metric("Verified", verified)
    with col3:
        st.metric("Likely", likely)
    with col4:
        st.metric("Possible", possible)
    with col5:
        avg_score = sum(l.lead_score for l in leads) / len(leads) if leads else 0
        st.metric("Avg Score", f"{avg_score:.2f}")
    
    # Leads table
    st.subheader("Leads Table")
    
    # Filter by status
    status_filter = st.multiselect(
        "Filter by Status",
        ["VERIFIED", "LIKELY", "POSSIBLE", "UNVERIFIED"],
        default=["VERIFIED", "LIKELY", "POSSIBLE"],
    )
    
    filtered_leads = [l for l in leads if l.status.value in status_filter]
    
    # Create dataframe
    df_data = []
    for lead in filtered_leads:
        df_data.append({
            "Company": lead.company_name,
            "Person": lead.person_name or "-",
            "Role": lead.role or "-",
            "Phone": lead.phone or "-",
            "Industry": lead.industry or "-",
            "City": lead.city or "-",
            "Lead Score": round(lead.lead_score, 2),
            "Status": lead.status.value,
        })
    
    df = pd.DataFrame(df_data)
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Lead Score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=1,
            ),
        }
    )
    
    # Export options
    st.subheader("📥 Export Results")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        if st.button("📊 Export to Excel", use_container_width=True):
            export_excel(filtered_leads)
    
    with col_export2:
        if st.button("📄 Export to JSON", use_container_width=True):
            export_json(filtered_leads)
    
    with col_export3:
        if st.button("📋 Export to CSV", use_container_width=True):
            export_csv(filtered_leads)


def export_excel(leads: list):
    """Export to Excel"""
    try:
        exporter = ExcelExporter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"/tmp/leads_{timestamp}.xlsx"
        exporter.export(leads, filepath)
        
        with open(filepath, 'rb') as f:
            st.download_button(
                label="Download Excel",
                data=f.read(),
                file_name=f"leads_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


def export_json(leads: list):
    """Export to JSON"""
    try:
        exporter = JSONExporter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"/tmp/leads_{timestamp}.json"
        exporter.export(leads, filepath)
        
        with open(filepath, 'r') as f:
            st.download_button(
                label="Download JSON",
                data=f.read(),
                file_name=f"leads_{timestamp}.json",
                mime="application/json",
            )
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


def export_csv(leads: list):
    """Export to CSV"""
    try:
        exporter = CSVExporter()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"/tmp/leads_{timestamp}.csv"
        exporter.export(leads, filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            st.download_button(
                label="Download CSV",
                data=f.read(),
                file_name=f"leads_{timestamp}.csv",
                mime="text/csv",
            )
    except Exception as e:
        st.error(f"Export failed: {str(e)}")


if __name__ == "__main__":
    main()
