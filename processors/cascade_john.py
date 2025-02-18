# processors/cascade_john.py
from .cascade_common import process as cascade_process

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    # Define New England states
    new_england_states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']

    # Filter the dataset to include only New England states
    df = df[df['Shipping State'].isin(new_england_states)]
    df = cascade_process(df)
    
    return df