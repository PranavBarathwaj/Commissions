# processors/cascade_john.py
from .cascade_common import process as cascade_process
import sys
import streamlit as st

def process(df):

    # Define New England states
    states = ['PA']

    # Filter the dataset to include only West Coast states
    df = df[df['Shipping State'].isin(states)]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program

    df = cascade_process(df)
    
    return df