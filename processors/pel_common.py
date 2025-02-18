import pandas as pd

# processors/pel_common.py
def process(pel):
    pel.insert(0, 'Account', 'N/A')
    pel.insert(1, 'Order Date', 'N/A')
    pel.insert(2, 'Order#', 'N/A')
    # Select only the specified columns
    columns_to_keep = ['Account', 'Order Date', 'Order#', 'Item', 'Qty', 'Ext Cost', 'Cost']
    pel = pel[columns_to_keep]

    pel = pel.rename(columns={
        'Item': 'Products Ordered',
        'Qty': 'QTY',
        'Ext Cost': 'Total',
        'Cost': 'Price Per Unit'
        # 'Subtotal' stays the same
    })

        # First, let's create lists of products for each category
    afo_products = ['ASLT', 'ASRT', 'AMLT', 'AMRT', 'ALLT', 'ALRT', 'AXLLT', 'AXLRT', 'SXSLT', 'SXSRT',
                    'SSLT', 'SSRT', 'SMLT', 'SMRT', 'SLLT', 'SLRT', 'SXLLT', 'SXLRT', 'PASLT', 'PASRT',
                    'PAMLT', 'PAMRT', 'PALLT', 'PALRT', 'PAXLLT', 'PAXLRT', 'MXSLT', 'MXSRT', 'MSLT',
                    'MSRT', 'MMLT', 'MMRT', 'MLLT', 'MLRT', 'MXLLT', 'MXLRT', 'FAXSRT', 'FAXSLT', 'FASLT',
                    'FASRT', 'FAMLT', 'FAMRT', 'FALLT', 'FALRT', 'FAXLLT', 'FAXLRT', 'UFOLT', 'UFORT',
                    'ASLT-MAG', 'ASRT-MAG', 'AMLT-MAG', 'AMRT-MAG', 'ALLT-MAG', 'ALRT-MAG', 'AXLLT-MAG',
                    'AXLRT-MAG', 'SXSLT-MAG', 'SXSRT-MAG', 'SSLT-MAG', 'SSRT-MAG', 'SMLT-MAG',
                    'SMRT-MAG', 'SLLT-MAG', 'SLRT-MAG', 'SXLLT-MAG', 'SXLRT-MAG', 'PASLT-MAG',
                    'PASRT-MAG', 'PAMLT-MAG', 'PAMRT-MAG', 'PALLT-MAG', 'PALRT-MAG', 'PAXLLT-MAG',
                    'PAXLRT-MAG', 'UFOLT-MAG', 'UFORT-MAG', 'MXSLT-MAG', 'MXSRT-MAG', 'MSLT-MAG',
                    'MSRT-MAG', 'MMLT-MAG', 'MMRT-MAG', 'MLLT-MAG', 'MLRT-MAG', 'MXLLT-MAG', 'MXLRT-MAG',
                    'FAXSRT-MAG', 'FAXSLT-MAG', 'FASLT-MAG', 'FASRT-MAG', 'FAMLT-MAG', 'FAMRT-MAG',
                    'FALLT-MAG', 'FALRT-MAG', 'FAXLLT-MAG', 'FAXLRT-MAG']

    iq_products = ['IQ-1001', 'IQ-1002', 'IQ-1003', 'IQ-1004']

    fp_products = ['FPFW5', 'FPW5', 'FPFW6', 'FPW6', 'FPFM6', 'FPM6', 'FPFM7', 'FPM7', 'FPFM8', 'FPM8', 
                'FPFM9', 'FPM9', 'FPFM10', 'FPM10', 'FPFM11', 'FPM11', 'FPFM12', 'FPM12', 'FPFM13', 
                'FPM13', 'FPFM14', 'FPM14', 'FPFM15', 'FPM15', 'FCCIS', 'CCIS', 'FCCIM', 'CCIM',
                'FCCIL', 'CCIL', 'FCCIXL', 'CCIXL', 'FKPF5', 'KFP5', 'FKFP6', 'KFP6', 'FKFP7', 'KFP7',
                'FKFP8', 'KFP8', 'FKFP9', 'KFP9', 'FKFP10', 'KFP10', 'FKFP11', 'KFP11', 'FKFP12',
                'KFP12', 'FKFPBK1', 'KFPBK1', 'FMEW5', 'RMEW5', 'FMEW6', 'RMEW6', 'FMEM6', 'RMEM6',
                'FMEM7', 'RMEM7', 'FMEM8', 'RMEM8', 'FMEM9', 'RMEM9', 'FMEM10', 'RMEM11', 'FMEM12',
                'RMEM12', 'FMEM13', 'RMEM13', 'FMEM14', 'RMEM14', 'FMEM15', 'RMEM15']

    ankle_braces_products = ['MACH-XS', 'MACH-S', 'MACH-M', 'MACH-L', 'MACH-XL',
                        'JET-XS', 'JET-S', 'JET-M', 'JET-L', 'JET-XL']

    tstrap_products = ['TS-L', 'TS-R']

    socks_products = ['SOCKAB', 'SOCKAB-3', 'SOCKAB-6', 'SOCKAB-12',
                    'SOCKAW', 'SOCKAW-6', 'SOCKAW-12']

    calf_sleeves_products = ['XFCSS', 'XFCSM', 'XFCSL', 'XFCSXL', 'XFCSXXL', 'XFCSXXXL']

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
        elif any(prod in tstrap_products for prod in products):
            return 'T-Strap'
        elif any(prod in socks_products for prod in products):
            return 'Socks'
        elif any(prod in calf_sleeves_products for prod in products):
            return 'Calf Sleeves'
        else:
            return 'Accessories'

    # Add Category column
    pel['Category'] = pel['Products Ordered'].apply(determine_category)

    # Reorder columns if needed
    pel = pel[['Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit']]

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

        elif category == 'T-Strap':
            if price < 15:
                return '10.00%'
            elif 15 <= price <= 19:
                return '15.00%'
            elif 20 <= price <= 23:
                return '20.00%'
            elif 24 <= price <= 28:
                return '22.50%'
            else:  # >= 29
                return '25.00%'

        elif category in ['Socks', 'Calf Sleeves']:
            if price <= 14:
                return '10.00%'
            elif 15 <= price <= 16:
                return '20.00%'
            elif 17 <= price <= 18:
                return '22.50%'
            else:  # >= 19
                return '25.00%'

        else:  # Accessories or any other category
            return '0.00%'

    # Add Bonus % column
    pel['Bonus %'] = pel.apply(determine_bonus_percentage, axis=1)

    # Reorder columns to include new Bonus % column
    pel = pel[['Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 'QTY', 'Total', 'Price Per Unit', 'Bonus %']]

    def calculate_bonus_pay(row):
        # Convert bonus percentage (e.g., '25.00%') to decimal (0.25)
        bonus_decimal = float(row['Bonus %'].strip('%')) / 100

        # Total is already a float, no need to convert
        total = float(row['Total'])

        # Calculate bonus pay (Total * bonus percentage)
        bonus_pay = total * bonus_decimal

        # Format as currency with 2 decimal places
        return f"${bonus_pay:.2f}"

    # Add Bonus Pay column
    pel['Bonus Pay'] = pel.apply(calculate_bonus_pay, axis=1)

    # Reorder columns to include new Bonus Pay column
    pel = pel[['Account', 'Order Date', 'Order#', 'Products Ordered', 'Category',
                            'QTY', 'Total', 'Price Per Unit', 'Bonus %', 'Bonus Pay']]

    return pel
