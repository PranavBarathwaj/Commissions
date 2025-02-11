import streamlit as st
import pandas as pd
import io
from config import COMPANIES, REPRESENTATIVES
from processors.registry import get_processor

def process_csv(df, company, rep_name):
    """Process CSV based on company and rep name"""
    processor = get_processor(company, rep_name)
    
    if processor:
        return processor(df)
    else:
        st.warning(f"No specific processing defined for {company} - {rep_name}")
        return df

def main():
    st.title("CSV File Processor")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Original Data")
        st.write(df.head())
        
        # Processing options
        st.subheader("Processing Options")
        
        company = st.selectbox(
            'Select Company',
            COMPANIES
        )
        
        rep_name = st.selectbox(
            'Select Representative',
            REPRESENTATIVES
        )
        
        # Show if processing exists for this combination
        processor = get_processor(company, rep_name)
        if processor:
            st.info(f"Processing method available for {company} - {rep_name}: {processor.__doc__}")
        else:
            st.warning(f"No specific processing defined for {company} - {rep_name}")
        
        if st.button("Process Data"):
            processed_df = process_csv(df, company, rep_name)
            
            st.subheader("Processed Data")
            st.write(processed_df.head())
            
            csv_buffer = io.StringIO()
            processed_df.to_csv(csv_buffer, index=False)
            csv_str = csv_buffer.getvalue()
            
            st.download_button(
                label="Download processed CSV",
                data=csv_str,
                file_name=f"processed_{company}_{rep_name}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()