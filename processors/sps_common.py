import pandas as pd

def process(sps):
    sps.insert(0, 'Account', 'N/A')
    sps = sps[sps['DROP_SHIP_FLAG'] == 'N']
    sps = sps[sps['Document_Type'] == 'Invoice Line']
    # Select only the specified columns
    columns_to_keep = ['STATE', 'CITY', 'Account', 'FULFILLMENT_DATE', 'ORDER_NUMBER', 'Part_Number', 'FULFILLED_QTY', 'Ea Cost']
    sps = sps[columns_to_keep]

    sps = sps.rename(columns={
        'FULFILLMENT_DATE': 'Order Date',
        'ORDER_NUMBER': 'Order#',
        'Part_Number': 'Products Ordered',
        'FULFILLED_QTY': 'QTY',
        'Ea Cost': 'Price Per Unit',
        'STATE': 'State',
        'CITY': 'City'
    })

    sps['Order Date'] = pd.to_datetime(sps['Order Date'], errors='coerce')
    sps['Order Date'] = sps['Order Date'].dt.strftime('%#m/%#d/%y')
    
    # Calculate Total for each line item
    sps['Total'] = sps['Price Per Unit'] * sps['QTY']
    
    # Sort by Order Date in descending order
    sps = sps.sort_values('Order Date', ascending=False)

    # First, let's create lists of products for each category
    afo_products = ['AXSRT', 'AXSLT', 'ASLT', 'ASRT', 'AMLT', 'AMRT', 'ALLT', 'ALRT', 'AXLLT', 'AXLRT', 'SXSLT', 'SXSRT',
                'SSLT', 'SSRT', 'SMLT', 'SMRT', 'SLLT', 'SLRT', 'SXLLT', 'SXLRT', 'PASLT', 'PASRT',
                'PAMLT', 'PAMRT', 'PALLT', 'PALRT', 'PAXLLT', 'PAXLRT', 'MXSLT', 'MXSRT', 'MSLT',
                'MSRT', 'MMLT', 'MMRT', 'MLLT', 'MLRT', 'MXLLT', 'MXLRT', 'FAXSRT', 'FAXSLT', 'FASLT',
                'FASRT', 'FAMLT', 'FAMRT', 'FALLT', 'FALRT', 'FAXLLT', 'FAXLRT', 'UFOLT', 'UFORT',
                'ASLTMAG', 'ASRTMAG', 'AMLTMAG', 'AMRTMAG', 'ALLTMAG', 'ALRTMAG', 'AXLLTMAG',
                'AXLRTMAG', 'SXSLTMAG', 'SXSRTMAG', 'SSLTMAG', 'SSRTMAG', 'SMLTMAG',
                'SMRTMAG', 'SLLTMAG', 'SLRTMAG', 'SXLLTMAG', 'SXLRTMAG', 'PASLTMAG',
                'PASRTMAG', 'PAMLTMAG', 'PAMRTMAG', 'PALLTMAG', 'PALRTMAG', 'PAXLLTMAG',
                'PAXLRTMAG', 'UFOLTMAG', 'UFORTMAG', 'MXSLT-MAG', 'MXSRT-MAG', 'MSLT-MAG',
                'MSRT-MAG', 'MMLT-MAG', 'MMRT-MAG', 'MLLT-MAG', 'MLRT-MAG', 'MXLLT-MAG', 'MXLRT-MAG',
                'FAXSRTMAG', 'FAXSLTMAG', 'FASLTMAG', 'FASRTMAG', 'FAMLTMAG', 'FAMRTMAG',
                'FALLTMAG', 'FALRTMAG', 'FAXLLTMAG', 'FAXLRTMAG']

    iq_products = ['IQ-1001', 'IQ-1002', 'IQ-1003', 'IQ-1004']

    fp_products = ['FPFW5-1', 'FPW5-1', 'FPFW6-1', 'FPW6-1', 'FPFM6-1', 'FPM6-1', 'FPFM7-1', 'FPM7-1', 'FPFM8-1', 'FPM8-1',
               'FPFM9-1', 'FPM9-1', 'FPFM10-1', 'FPM10-1', 'FPFM11-1', 'FPM11-1', 'FPFM12-1', 'FPM12-1', 'FPFM13-1',
               'FPM13-1', 'FPFM14-1', 'FPM14-1', 'FPFM15-1', 'FPM15-1', 'FPFW5', 'FPW5', 'FPFW6', 'FPW6', 'FPFM6', 'FPM6', 
               'FPFM7', 'FPM7', 'FPFM8', 'FPM8', 'FPFM9', 'FPM9', 'FPFM10', 'FPM10', 'FPFM11', 'FPM11', 'FPFM12', 'FPM12', 
               'FPFM13', 'FPM13', 'FPFM14', 'FPM14', 'FPFM15', 'FPM15', 'FCCIS', 'CCIS', 'FCCIM', 'CCIM',
               'FCCIL', 'CCIL', 'FCCIXL', 'CCIXL', 'FKPF5', 'KFP5', 'FKFP6', 'KFP6', 'FKFP7', 'KFP7',
               'FKFP8', 'KFP8', 'FKFP9', 'KFP9', 'FKFP10', 'KFP10', 'FKFP11', 'KFP11', 'FKFP12',
               'KFP12', 'FKFPBK1', 'KFPBK1', 'FMEW5', 'RMEW5', 'FMEW6', 'RMEW6', 'FMEM6', 'RMEM6',
               'FMEM7', 'RMEM7', 'FMEM8', 'RMEM8', 'FMEM9', 'RMEM9', 'FMEM10', 'RMEM10', 'FMEM11', 'RMEM11', 'FMEM12',
               'RMEM12', 'FMEM13', 'RMEM13', 'FMEM14', 'RMEM14', 'FMEM15', 'RMEM15']

    ankle_braces_products = ['MACH-XS', 'MACH-S', 'MACH-M', 'MACH-L', 'MACH-XL',
                        'JET-XS', 'JET-S', 'JET-M', 'JET-L', 'JET-XL']

    tstrap_products = ['TS-L', 'TS-R']

    socks_products = ['SOCKAB', 'SOCKAB-3', 'SOCKAB-6', 'SOCKAB-12', 
                    'SOCKAW', 'SOCKAW-6', 'SOCKAW-12']

    calf_sleeves_products = ['XFCSS', 'XFCSM', 'XFCSL', 'XFCSXL', 'XFCSXXL', 'XFCSXXXL']

    def determine_category(product):
        if product in afo_products:
            return 'AFO'
        elif product in iq_products:
            return 'IQ'
        elif product in fp_products:
            return 'FP'
        elif product in ankle_braces_products:
            return 'Ankle Braces'
        elif product in tstrap_products:
            return 'T-Strap'
        elif product in socks_products:
            return 'Socks'
        elif product in calf_sleeves_products:
            return 'Calf Sleeves'
        else:
            return 'Accessories'
        
    # Add Category column - now just looking at the single product
    sps['Category'] = sps['Products Ordered'].apply(determine_category)

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
    sps['Bonus %'] = sps.apply(determine_bonus_percentage, axis=1)

    def calculate_bonus_pay(row):
        # Convert bonus percentage (e.g., '25.00%') to decimal (0.25)
        bonus_decimal = float(row['Bonus %'].strip('%')) / 100
        
        # Total is already a float, no need to convert
        total = row['Total']
        
        # Calculate bonus pay (Total * bonus percentage)
        bonus_pay = total * bonus_decimal
        
        # Format as currency with 2 decimal places
        return f"${bonus_pay:.2f}"

    # Add Bonus Pay column
    sps['Bonus Pay'] = sps.apply(calculate_bonus_pay, axis=1)

    # Reorder columns for the final output
    result = sps[['State', 'City', 'Account', 'Order Date', 'Order#', 'Products Ordered', 'Category', 
                  'QTY', 'Total', 'Price Per Unit', 'Bonus %', 'Bonus Pay']]
    
    return result