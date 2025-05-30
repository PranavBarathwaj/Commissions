import pandas as pd

# processors/shopify_common.py
def process(shopify):
    # Select only the specified columns
    columns_to_keep = ['Shipping Name', 'Shipping Company', 'Created at', 'Name', 'Lineitem sku', 'Lineitem quantity', 'Lineitem price', 'Subtotal','Shipping Province', 'Shipping City', 'Shipping Zip']
    shopify = shopify[columns_to_keep]

    # Rename columns
    shopify = shopify.rename(columns={
        'Created at': 'Order Date',
        'Name': 'Order#',
        'Lineitem sku': 'Products Ordered',
        'Lineitem quantity': 'QTY',
        'Lineitem price': 'Unit Price',
        'Subtotal': 'Total',
        'Shipping Province': 'State',
        'Shipping City': 'City',
        'Shipping Zip': 'Zip'
    })
    
    # Create Account column with Shipping Company, defaulting to Shipping Name when empty
    shopify['Account'] = shopify['Shipping Company'].fillna(shopify['Shipping Name'])
    
    # Drop the original columns since we've processed them
    shopify = shopify.drop(['Shipping Company', 'Shipping Name'], axis=1)


    # First check if the column has the correct data type
    # Convert to datetime format with better error handling
    try:
        shopify['Order Date'] = pd.to_datetime(shopify['Order Date'], errors='coerce')
        # Only apply dt.strftime to non-null values
        mask = shopify['Order Date'].notna()
        if mask.any():  # If there are any valid datetime values
            shopify.loc[mask, 'Order Date'] = shopify.loc[mask, 'Order Date'].dt.strftime('%m/%d/%y')
        else:
            # If all values are NaT, convert column to string to avoid dt accessor errors
            shopify['Order Date'] = shopify['Order Date'].astype(str)
    except Exception as e:
        # If conversion fails entirely, set to string
        shopify['Order Date'] = shopify['Order Date'].astype(str)
    
    # Handle nulls in Products Ordered - convert to empty string instead of null
    shopify['Products Ordered'] = shopify['Products Ordered'].fillna('')
    
    def combine_products_with_qty(group):
        products_list = []
        for prod, qty in zip(group['Products Ordered'], group['QTY']):
            # Skip empty product names
            if not prod:
                continue
                
            # Convert prod to string explicitly in case it's a float or other non-string type
            prod_str = str(prod)
            
            # Format with quantity if qty > 1
            if qty > 1:
                products_list.append(f"{prod_str}x{int(qty)}")
            else:
                products_list.append(prod_str)
                
        # Join all products with a comma
        return ", ".join(products_list) if products_list else ""

    # Make sure Total and QTY are numeric before grouping
    shopify['Total'] = pd.to_numeric(shopify['Total'], errors='coerce').fillna(0)
    shopify['QTY'] = pd.to_numeric(shopify['QTY'], errors='coerce').fillna(0)
    shopify['Unit Price'] = pd.to_numeric(shopify['Unit Price'], errors='coerce').fillna(0)
    
    # Create a new QTY column that is 0 for items with zero price
    shopify.loc[shopify['Unit Price'] <= 0, 'QTY'] = 0

    # Group by order number and aggregate the data
    consolidated = shopify.groupby('Order#').agg({
        'Account': 'first',
        'Order Date': 'first',
        'Products Ordered': lambda x: combine_products_with_qty(pd.DataFrame({
            'Products Ordered': x.values,
            'QTY': shopify.loc[x.index, 'QTY'].values
        })),
        'QTY': 'sum',
        'Total': 'sum',  # Changed from 'first' to 'sum' to add up all subtotals
        'State': 'first',
        'City': 'first',
        'Zip': 'first',
    }).reset_index()

    # Make sure Total and QTY are numeric for division
    consolidated['Total'] = pd.to_numeric(consolidated['Total'], errors='coerce')
    consolidated['QTY'] = pd.to_numeric(consolidated['QTY'], errors='coerce')
    
    # Add Price Per Unit column with error handling
    consolidated['Price Per Unit'] = 0.0  # Default value
    # Only calculate where QTY is valid and greater than 0
    mask = (consolidated['QTY'] > 0) & consolidated['QTY'].notna() & consolidated['Total'].notna()
    consolidated.loc[mask, 'Price Per Unit'] = consolidated.loc[mask, 'Total'] / consolidated.loc[mask, 'QTY']

    # Round Price Per Unit to 2 decimal places
    consolidated['Price Per Unit'] = consolidated['Price Per Unit'].round(2)

    # Sort by Order Date (safely)
    try:
        consolidated = consolidated.sort_values('Order Date', ascending=False)
    except:
        # If sort fails, continue without sorting
        pass
    
    # First, let's create lists of products for each category
    afo_products = ['AXSRT', 'AXSLT', 'ASLT', 'ASRT', 'AMLT', 'AMRT', 'ALLT', 'ALRT', 'AXLLT', 'AXLRT', 'SXSLT', 'SXSRT',
                'SSLT', 'SSRT', 'SMLT', 'SMRT', 'SLLT', 'SLRT', 'SXLLT', 'SXLRT', 'PAXSRT', 'PAXSLT', 'PASLT', 'PASRT',
                'PAMLT', 'PAMRT', 'PALLT', 'PALRT', 'PAXLLT', 'PAXLRT', 'MXSLT', 'MXSRT', 'MSLT',
                'MSRT', 'MMLT', 'MMRT', 'MLLT', 'MLRT', 'MXLLT', 'MXLRT', 'FAXSRT', 'FAXSLT', 'FASLT',
                'FASRT', 'FAMLT', 'FAMRT', 'FALLT', 'FALRT', 'FAXLLT', 'FAXLRT', 'UFOLT', 'UFORT',
                'AXSLRT-MAG', 'AXSRT-MAG', 'AXSLT-MAG', 'ASLT-MAG', 'ASRT-MAG', 'AMLT-MAG', 'AMRT-MAG', 'ALLT-MAG', 'ALRT-MAG', 'AXLLT-MAG',
                'AXLRT-MAG', 'SXSLT - MAG', 'SXSRT - MAG', 'SSLT - MAG', 'SSRT - MAG', 'SMLT - MAG',
                'SMRT - MAG', 'SLLT - MAG', 'SLRT - MAG', 'SXLLT - MAG', 'SXLRT - MAG', 'PAXSRT-MAG', 'PAXSLT-MAG', 'PASLT-MAG',
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
        # Return 'Accessories' for empty strings
        if not products_str:
            return 'Accessories'
            
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
    consolidated = consolidated[['State', 'City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit', 'Zip']]

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
            else:  # >= 73
                return '18.00%'
        else:  # Accessories or any other category
            return '0.00%'

    # Add Bonus % column
    consolidated['Bonus %'] = consolidated.apply(determine_bonus_percentage, axis=1)

    # Reorder columns to include new Bonus % column
    consolidated = consolidated[['State','City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit', 'Bonus %', 'Zip']]

    def calculate_bonus_pay(row):
        try:
            # Convert bonus percentage (e.g., '25.00%') to decimal (0.25)
            bonus_decimal = float(row['Bonus %'].strip('%')) / 100
            
            # Ensure Total is numeric
            total = pd.to_numeric(row['Total'], errors='coerce')
            if pd.isna(total):
                return '$0.00'
            
            # Calculate bonus pay (Total * bonus percentage)
            bonus_pay = total * bonus_decimal
            
            # Format as currency with 2 decimal places
            return f"${bonus_pay:.2f}"
        except:
            return '$0.00'

    # Add Bonus Pay column
    consolidated['Bonus Pay'] = consolidated.apply(calculate_bonus_pay, axis=1)

    # Reorder columns to include new Bonus Pay column
    consolidated = consolidated[['State','City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 
                            'QTY', 'Total', 'Price Per Unit', 'Bonus %', 'Bonus Pay', 'Zip']]

    return consolidated