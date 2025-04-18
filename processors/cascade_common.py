import pandas as pd
import numpy as np

# processors/cascade_common.py
def process(cascade):

    cascade = cascade.copy()
    cascade.columns = cascade.columns.str.strip()
    numeric_columns = ['Quantity', 'Total Price', 'Cogs_Amount']
    cascade[numeric_columns] = cascade[numeric_columns].replace({r'[\$\(\),]': ''}, regex=True)

    # Convert numeric columns to proper numeric types
    for col in numeric_columns:
        cascade[col] = pd.to_numeric(cascade[col], errors='coerce')
    
    # Convert Quantity specifically to Int64
    cascade['Quantity'] = cascade['Quantity'].astype('Int64')
    
    # Filter only direct shipment = N
    cascade = cascade[cascade['Direct Shipment'] == 'N']
    
    # Select only the specified columns
    columns_to_keep = ['Shipping State', 'Shipping City', 'Account Name', 'Invoice Date', 'Sales Name', 'Product Code', 'Quantity', 'Cogs_Amount']
    cascade = cascade[columns_to_keep]

    cascade = cascade.rename(columns={
        'Account Name': 'Account',
        'Invoice Date': 'Order Date',
        'Sales Name': 'Order#',
        'Product Code': 'Products Ordered',
        'Quantity': 'QTY',
        'Cogs_Amount': 'Total',
        'Shipping State': 'State',
        'Shipping City': 'City'
    })

    cascade['Order Date'] = pd.to_datetime(cascade['Order Date'], errors='coerce')
    cascade['Order Date'] = cascade['Order Date'].dt.strftime('%#m/%#d/%y')

    def combine_products_with_qty(group):
        products = []
        for prod, qty in zip(group['Products Ordered'], group['QTY']):
            # Fix: Check if qty is NA/null first, before comparing
            if pd.isna(qty):
                products.append(str(prod))
            elif qty <= 1:  # Only do comparison when qty is not NA
                products.append(str(prod))
            else:
                products.append(f"{prod}x{int(qty)}")
        return ', '.join(products)

    # Group by order number and aggregate the data
    # IMPORTANT FIX: Ensure that numeric columns are properly converted before aggregation
    # Make sure the Total column is numeric before aggregation
    cascade['Total'] = pd.to_numeric(cascade['Total'], errors='coerce')
    
    # Create a temporary dataframe to help with the Products Ordered aggregation
    temp_df = cascade.copy()
    
    # Group by order number - using explicit aggregation functions that handle nulls properly
    consolidated = cascade.groupby('Order#', as_index=False).agg({
        'Account': 'first',
        'Order Date': 'first',
        'QTY': lambda x: x.sum(skipna=True),
        'Total': lambda x: x.sum(skipna=True),  # Critical fix: use sum with skipna=True
        'State': 'first',
        'City': 'first'
    })
    
    # Special handling for Products Ordered
    products_combined = {}
    for order_num, group in temp_df.groupby('Order#'):
        products_combined[order_num] = combine_products_with_qty(group)
    
    # Add the combined products to the consolidated dataframe
    consolidated['Products Ordered'] = consolidated['Order#'].map(products_combined)

    # Add Price Per Unit column with safe division
    # Initialize with zeros then only calculate for valid rows
    consolidated['Price Per Unit'] = 0.0
    # Only calculate Price Per Unit where QTY > 0 and Total is not null
    mask = (consolidated['QTY'] > 0) & (~consolidated['Total'].isna())
    consolidated.loc[mask, 'Price Per Unit'] = (consolidated.loc[mask, 'Total'] / consolidated.loc[mask, 'QTY']).round(2)

    # First, let's create lists of products for each category
    afo_products = ['AXSRT', 'AXSLT', 'ASLT', 'ASRT', 'AMLT', 'AMRT', 'ALLT', 'ALRT', 'AXLLT', 'AXLRT', 'SXSLT', 'SXSRT',
                'SSLT', 'SSRT', 'SMLT', 'SMRT', 'SLLT', 'SLRT', 'SXLLT', 'SXLRT', 'PAXSRT', 'PAXSLT', 'PASLT', 'PASRT',
                'PAMLT', 'PAMRT', 'PALLT', 'PALRT', 'PAXLLT', 'PAXLRT', 'MXSLT', 'MXSRT', 'MSLT',
                'MSRT', 'MMLT', 'MMRT', 'MLLT', 'MLRT', 'MXLLT', 'MXLRT', 'FAXSRT', 'FAXSLT', 'FASLT',
                'FASRT', 'FAMLT', 'FAMRT', 'FALLT', 'FALRT', 'FAXLLT', 'FAXLRT', 'UFOLT', 'UFORT',
                'AXSLRT-MAG', 'AXSRT-MAG', 'AXSLT-MAG', 'ASLT-MAG', 'ASRT-MAG', 'AMLT-MAG', 'AMRT-MAG', 'ALLT-MAG', 'ALRT-MAG', 'AXLLT-MAG',
                'AXLRT-MAG', 'SXSLT-MAG', 'SXSRT-MAG', 'SSLT-MAG', 'SSRT-MAG', 'SMLT-MAG',
                'SMRT-MAG', 'SLLT-MAG', 'SLRT-MAG', 'SXLLT-MAG', 'SXLRT-MAG', 'PAXSRT-MAG', 'PAXSLT-MAG', 'PASLT-MAG',
                'PASRT-MAG', 'PAMLT-MAG', 'PAMRT-MAG', 'PALLT-MAG', 'PALRT-MAG', 'PAXLLT-MAG',
                'PAXLRT-MAG', 'UFOLT-MAG', 'UFORT-MAG', 'MXSLT-MAG', 'MXSRT-MAG', 'MSLT-MAG',
                'MSRT-MAG', 'MMLT-MAG', 'MMRT-MAG', 'MLLT-MAG', 'MLRT-MAG', 'MXLLT-MAG', 'MXLRT-MAG',
                'FAXSRT-MAG', 'FAXSLT-MAG', 'FASLT-MAG', 'FASRT-MAG', 'FAMLT-MAG', 'FAMRT-MAG',
                'FALLT-MAG', 'FALRT-MAG', 'FAXLLT-MAG', 'FAXLRT-MAG']

    iq_products = ['IQ-1001', 'IQ-1002', 'IQ-1003', 'IQ-1004']

    fp_products = ['FPFW5-1', 'FPW5-1', 'FPFW6-1', 'FPW6-1', 'FPFM6-1', 'FPM6-1', 'FPFM7-1', 'FPM7-1', 'FPFM8-1', 'FPM8-1', 'FPW5', 'FPW6', 'FPM6', 'FPM7', 'FPM8', 'FPM9', 'FPM10', 'FPM11', 'FPM12', 'FPM13', 'FPM14', 'FPM15', 'FPM16',
               'FPFM9-1', 'FPM9-1', 'FPFM10-1', 'FPM10-1', 'FPFM11-1', 'FPM11-1', 'FPFM12-1', 'FPM12-1', 'FPFM13-1', 'FPFW5', 'FPFW6', 'FPFM6', 'FPFM7', 'FPFM8', 'FPFM9', 'FPFM10', 'FPFM11', 'FPFM12', 'FPFM13', 'FPFM14', 'FPFM15', 'FPFM16',
               'FPM13-1', 'FPFM14-1', 'FPM14-1', 'FPFM15-1', 'FPM15-1', 'FPFM16-1', 'FPM16-1', 'FCCIS', 'CCIS', 'FCCIM', 'CCIM',
               'FCCIL', 'CCIL', 'FCCIXL', 'CCIXL', 'FKFP5', 'KFP5', 'FKFP6', 'KFP6', 'FKFP7', 'KFP7',
               'FKFP8', 'KFP8', 'FKFP9', 'KFP9', 'FKFP10', 'KFP10', 'FKFP11', 'KFP11', 'FKFP12',
               'KFP12', 'FKFPBK1', 'KFPBK1', 'FMEW5', 'RMEW5', 'FMEW6', 'RMEW6', 'FMEM6', 'RMEM6',
               'FMEM7', 'RMEM7', 'FMEM8', 'RMEM8', 'FMEM9', 'RMEM9', 'FMEM10', 'RMEM10', 'FMEM11', 'RMEM11', 'FMEM12',
               'RMEM12', 'FMEM13', 'RMEM13', 'FMEM14', 'RMEM14', 'FMEM15', 'RMEM15',
               'W6', 'FLXW7M6', 'FLXW8M7', 'FLXW9M8', 'FLXW10M9', 'FLXW11M10', 'FLXW12M11', 'FLXW13M12', 'FLXW14M13', 'FLXM14', 'FLXM15', 'FLXM16']

    ankle_braces_products = ['MACH-XS', 'MACH-S', 'MACH-M', 'MACH-L', 'MACH-XL',
                        'JET-XS', 'JET-S', 'JET-M', 'JET-L', 'JET-XL']

    # tstrap_products = ['TS-L', 'TS-R']

    # socks_products = ['SOCKAB', 'SOCKAB-3', 'SOCKAB-6', 'SOCKAB-12',
    #                 'SOCKAW', 'SOCKAW-6', 'SOCKAW-12']

    # calf_sleeves_products = ['XFCSS', 'XFCSM', 'XFCSL', 'XFCSXL', 'XFCSXXL', 'XFCSXXXL']

    def determine_category(products_str):
        # Remove quantity indicators and split into individual products
        products = [p.split('x')[0].strip() for p in products_str.split(',')]

        if any(prod in afo_products for prod in products):
            return 'AFO'
        elif any(prod in iq_products for prod in products):
            return 'IQ'
        elif any(prod in fp_products for prod in products):
            return 'FP'
        elif any(prod in ankle_braces_products for prod in products):
            return 'Ankle Braces'
        # elif any(prod in tstrap_products for prod in products):
        #     return 'T-Strap'
        # elif any(prod in socks_products for prod in products):
        #     return 'Socks'
        # elif any(prod in calf_sleeves_products for prod in products):
        #     return 'Calf Sleeves'
        else:
            return 'Accessories'

    # Add Category column
    consolidated['Category'] = consolidated['Products Ordered'].apply(determine_category)

    # Reorder columns if needed
    consolidated = consolidated[['State', 'City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit']]

    def determine_bonus_percentage(row):
        # Price Per Unit is already a float, no need to convert
        price = row['Price Per Unit']
        category = row['Category']

        if category == 'AFO':
            if price < 229:
                return '10.00%'
            elif 229 <= price <= 258:
                return '15.00%'
            elif 259 <= price <= 298:
                return '20.00%'
            elif 299 <= price <= 348:
                return '22.50%'
            else:  # >= 349
                return '25.00%'

        elif category == 'FP':
            if price < 19:
                return '10.00%'
            elif 19 <= price <= 22:
                return '15.00%'
            elif 23 <= price <= 25:
                return '20.00%'
            elif 26 <= price <= 29:
                return '22.50%'
            else:  # >= 30
                return '25.00%'

        elif category == 'Ankle Braces':
            if price <= 14:
                return '10.00%'
            elif 15 <= price <= 16:
                return '12.50%'
            elif 17 <= price <= 18:
                return '15.00%'
            else:  # >= 19
                return '25.00%'

        # elif category == 'T-Strap':
        #     if price < 15:
        #         return '10.00%'
        #     elif 15 <= price <= 19:
        #         return '15.00%'
        #     elif 20 <= price <= 23:
        #         return '20.00%'
        #     elif 24 <= price <= 28:
        #         return '22.50%'
        #     else:  # >= 29
        #         return '25.00%'

        # elif category in ['Socks', 'Calf Sleeves']:
        #     if price <= 14:
        #         return '10.00%'
        #     elif 15 <= price <= 16:
        #         return '20.00%'
        #     elif 17 <= price <= 18:
        #         return '22.50%'
        #     else:  # >= 19
        #         return '25.00%'
        
        elif category == 'IQ':
            if 65.5 <= price <= 69:
                return '10.00%'
            elif 69.25 <= price <= 72:
                return '15.00%'
            else:   # >= 73
                return '18.00%'   

        else:  # Accessories or any other category
            return '0.00%'

    # Add Bonus % column
    consolidated['Bonus %'] = consolidated.apply(determine_bonus_percentage, axis=1)

    # Reorder columns to include new Bonus % column
    consolidated = consolidated[['State', 'City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit', 'Bonus %']]

    def calculate_bonus_pay(row):
        # Convert bonus percentage (e.g., '25.00%') to decimal (0.25)
        bonus_decimal = float(row['Bonus %'].strip('%')) / 100

        # Total is already a float, no need to convert
        total = row['Total']
        
        # Handle NaN values
        if pd.isna(total):
            return '$0.00'

        # Calculate bonus pay (Total * bonus percentage)
        bonus_pay = total * bonus_decimal

        # Format as currency with 2 decimal places
        return f"${bonus_pay:.2f}"

    # Add Bonus Pay column
    consolidated['Bonus Pay'] = consolidated.apply(calculate_bonus_pay, axis=1)

    # Reorder columns to include new Bonus Pay column
    consolidated = consolidated[['State', 'City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category',
                            'QTY', 'Total', 'Price Per Unit', 'Bonus %', 'Bonus Pay']]

    return consolidated