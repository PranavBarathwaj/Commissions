# processors/sps_jon.py
from .sps_common import process as sps_process
import sys
import streamlit as st
import pandas as pd

def process(df):
    
    # First apply common Shopify processing
    # Define New England states
    states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']

    # Filter the dataset to include only New England states
    df = df[df['STATE'].isin(states)]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program

    df = sps_process(df)
    
    return df