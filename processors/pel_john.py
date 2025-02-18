# processors/cascade_john.py
from .pel_common import process as pel_process

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    # Define New England states
    new_england_states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']

    # Filter the dataset to include only New England states
    df = df[df['State:'].isin(new_england_states)]
    df = pel_process(df)
    
    return df