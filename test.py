import streamlit as st
import pandas as pd
import io
from config import COMPANIES, REPRESENTATIVES
from processors.registry import get_processor

def setup_page_config():
    """Configure basic page settings"""
    st.set_page_config(
        page_title="CSV Processor",
        page_icon="📊",
        layout="wide"
    )

def show_data_preview(df, title):
    """Display data preview with additional information"""
    with st.expander(f"{title} (Click to expand)", expanded=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df.head(), use_container_width=True)

def render_sidebar():
    """Render sidebar with processing options"""
    with st.sidebar:
        st.header("⚙️ Processing Options")
        
        company = st.selectbox(
            'Select Company',
            COMPANIES,
            help="Choose the company whose data format you're working with"
        )
        
        rep_name = st.selectbox(
            'Select Representative',
            REPRESENTATIVES,
            help="Select the representative associated with this data"
        )
        
        processor = get_processor(company, rep_name)
        if processor:
            st.success(f"✅ Processing method available for {company} - {rep_name}")
        else:
            st.error(f"❌ No specific processing defined for {company} - {rep_name}")
            
        return company, rep_name

def process_and_download(df, company, rep_name):
    """Process data and provide download option"""
    processed_df = process_csv(df, company, rep_name)
    
    # Display processed data
    show_data_preview(processed_df, "Processed Data")
    
    # Prepare download
    csv_buffer = io.StringIO()
    processed_df.to_csv(csv_buffer, index=False)
    csv_str = csv_buffer.getvalue()
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(
            label="📥 Download Processed CSV",
            data=csv_str,
            file_name=f"processed_{company}_{rep_name}.csv",
            mime="text/csv",
            use_container_width=True
        )

def process_csv(df, company, rep_name):
    """Process CSV based on company and rep name"""
    processor = get_processor(company, rep_name)
    
    if processor:
        with st.spinner('Processing data...'):
            return processor(df)
    else:
        st.warning(f"No specific processing defined for {company} - {rep_name}")
        return df

def main():
    setup_page_config()
    
    # Main header with styling
    st.title("📊 Commissions Report Formatter")
    st.markdown("""
    Transform your CSV files according to company-specific requirements.
    Upload your file below to get started.
    """)
    
    # Sidebar processing options
    company, rep_name = render_sidebar()
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload a CSV file to process"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            show_data_preview(df, "Original Data")
            
            if st.button("🔄 Process Data", use_container_width=True):
                process_and_download(df, company, rep_name)
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.stop()
    else:
        # Show placeholder when no file is uploaded
        st.info("👆 Please upload a CSV file to begin processing")

if __name__ == "__main__":
    main()