# processors/pel_kyle.py
from .pel_common import process as pel_process
import sys
import streamlit as st
import pandas as pd

def process(df):
    
    states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']
    
    # Filter the dataset to include only West Coast states
    df = df[df['State'].isin(states)]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program
    
    # If we have data, continue with processing
    df = pel_process(df)
    
    return df