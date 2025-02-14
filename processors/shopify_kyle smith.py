# processors/shopify_john.py
from .shopify_common import process as shopify_process

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    df = shopify_process(df)
    
    return df