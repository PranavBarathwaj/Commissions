# processors/shopify_common

import pandas as pd
from .consolidated_common import consolidated_common

def process(shopify):
    """Process for SPS - John combination"""
    # Select only the specified columns
    columns_to_keep = ['Shipping Name', 'Created at', 'Name', 'Lineitem sku', 'Lineitem quantity', 'Subtotal']
    shopify = shopify[columns_to_keep]

    shopify = shopify.rename(columns={
        'Shipping Name': 'Account',
        'Created at': 'Order Date',
        'Name': 'Order#',
        'Lineitem sku': 'Products Ordered',
        'Lineitem quantity': 'QTY',
        'Subtotal': 'Total'
        # 'Subtotal' stays the same
    })

    # Convert to datetime format
    shopify['Order Date'] = pd.to_datetime(shopify['Order Date'], errors='coerce')
    shopify['Order Date'] = shopify['Order Date'].dt.strftime('%#m/%#d/%y')

    return(consolidated_common(shopify))