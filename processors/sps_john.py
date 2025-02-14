# processors/sps_john.py
from .sps_common import process as sps_process

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    # Define New England states
    new_england_states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']

    # Filter the dataset to include only New England states
    df = df[df['STATE'].isin(new_england_states)]
    df = sps_process(df)
    
    return df