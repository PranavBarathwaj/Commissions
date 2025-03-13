# processors/sps_jon.py
from .sps_common import process as sps_process
import sys
import streamlit as st

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    # Define New England states
    states = ['ND', 'SD', 'MN', 'IA', 'NE']

    # Filter the dataset to include only New England states
    df = df[df['STATE'].isin(states)]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program

    df = sps_process(df)
    
    return df