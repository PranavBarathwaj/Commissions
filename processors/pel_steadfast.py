# processors/pel_kyle.py
from .pel_common import process as pel_process
import sys
import streamlit as st

def process(df):
    """Shopify processing for John with additional customization"""
    # Define West Coast states
    states = ['ND', 'SD', 'MN', 'IA', 'OR']
    
    # Filter the dataset to include only West Coast states
    df = df[df['State:'].isin(states)]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program
    
    # If we have data, continue with processing
    df = pel_process(df)
    
    return df