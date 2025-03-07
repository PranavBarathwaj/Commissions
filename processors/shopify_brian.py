# processors/shopify_jon.py
from .shopify_common import process as shopify_process

def process(df):
    """Shopify processing for John with additional customization"""
    # First apply common Shopify processing
    
    df['Shipping Zip'] = df['Shipping Zip'].str.replace("^'", "", regex=True)
    
    zip = [
    # Baldwin County, Alabama
    '36507', '36511', '36526', '36527', '36530', '36532', '36533', '36535', '36536', '36542', '36547', '36549',
    '36550', '36551', '36555', '36559', '36561', '36562', '36564', '36567', '36568', '36571', '36576', '36577',
    '36578', '36579', '36580', '36590', '36602', '36603', '36606', '36608', '36509', '36528',
    
    # Mobile County, Alabama
    '36505', '36509', '36511', '36512', '36521', '36522', '36523', '36525', '36528', '36530', '36541', '36544',
    '36560', '36571', '36572', '36575', '36582', '36587', '36590', '36601', '36602', '36603', '36604', '36605',
    '36606', '36607', '36608', '36609', '36610', '36611', '36612', '36613', '36615', '36616', '36617', '36618',
    '36619', '36620', '36621', '36622', '36625', '36628', '36630', '36633', '36640', '36641', '36644', '36652',
    '36660', '36663', '36670', '36671', '36675', '36685', '36688', '36689', '36691', '36693', '36695', '36701',
    
    # Escambia County, Florida
    '32501', '32502', '32503', '32504', '32505', '32506', '32507', '32508', '32509', '32511', '32512', '32513',
    '32514', '32516', '32520', '32521', '32522', '32523', '32524', '32526', '32534', '32535', '32559', '32560',
    '32561', '32562', '32563', '32570', '32577', '32591', '32592', '32593', '32594', '32595', '32596', '32597',
    '32598', '32530', '32533', '32568', '32571', '32583'
    ]
    
    # Create masks for different filtering conditions
    mask_la_ms = df['Shipping Province'].isin(['LA', 'MS'])  # No zip filtering for LA, MS, and PA
    mask_al_fl = (df['Shipping Province'].isin(['AL', 'FL'])) & (df['Shipping Zip'].isin(zip))  # Zip filtering for AL and FL
    
    # Combine masks with OR operator
    combined_mask = mask_la_ms | mask_al_fl
    
    # Apply the filter
    df = df[combined_mask]

    df = shopify_process(df)
    
    return df