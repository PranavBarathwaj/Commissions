# processors/pel_kyle.py
from .pel_common import process as pel_process
import sys
import streamlit as st

def process(df):
    """Shopify processing for John with additional customization"""
    # Define West Coast states
    states = ['PA']
    zip= [
    # Allegheny County
    '15006', '15007', '15014', '15015', '15017', '15018', '15020', '15024', '15025', '15026', '15028', '15030', 
    '15031', '15032', '15034', '15035', '15037', '15044', '15045', '15046', '15047', '15049', '15051', '15056', 
    '15057', '15063', '15064', '15065', '15071', '15075', '15076', '15082', '15084', '15085', '15086', '15088', 
    '15090', '15091', '15095', '15096', '15101', '15102', '15104', '15106', '15108', '15110', '15112', '15116', 
    '15120', '15122', '15123', '15126', '15127', '15129', '15131', '15132', '15133', '15134', '15135', '15136', 
    '15137', '15139', '15140', '15142', '15143', '15144', '15145', '15146', '15147', '15148',
    '15201', '15202', '15203', '15204', '15205', '15206', '15207', '15208', '15209', '15210', '15211', '15212',
    '15213', '15214', '15215', '15216', '15217', '15218', '15219', '15220', '15221', '15222', '15223', '15224',
    '15225', '15226', '15227', '15228', '15229', '15230', '15231', '15232', '15233', '15234', '15235', '15236',
    '15237', '15238', '15239', '15240', '15241', '15242', '15243', '15244', '15250', '15251', '15252', '15253',
    '15254', '15255', '15257', '15258', '15259', '15260', '15261', '15262', '15264', '15265', '15267', '15268',
    '15270', '15272', '15274', '15275', '15276', '15277', '15278', '15279', '15281', '15282', '15283', '15286',
    '15289', '15290', '15295',
    
    # Beaver County
    '15001', '15003', '15009', '15010', '15027', '15042', '15043', '15050', '15052', '15053', '15059', '15061',
    '15066', '15074', '15081', '16123',
    
    # Butler County
    '16001', '16002', '16003', '16016', '16020', '16021', '16022', '16023', '16024', '16025', '16027', '16028',
    '16029', '16030', '16033', '16034', '16035', '16037', '16038', '16039', '16040', '16041', '16045', '16046',
    '16048', '16049', '16050', '16051', '16052', '16053', '16054', '16055', '16056', '16057', '16058', '16059',
    '16061', '16063', '16066',
    
    # Washington County
    '15012', '15019', '15021', '15022', '15032', '15033', '15301', '15310', '15311', '15312', '15313', '15314',
    '15315', '15316', '15317', '15320', '15321', '15322', '15323', '15324', '15325', '15327', '15329', '15330',
    '15331', '15332', '15333', '15334', '15335', '15336', '15337', '15338', '15339', '15340', '15341', '15342',
    '15343', '15344', '15345', '15346', '15347', '15348', '15349', '15350', '15351', '15352', '15353', '15354',
    '15355', '15356', '15357', '15358', '15359', '15360', '15361', '15362', '15363', '15364', '15365', '15366',
    '15367', '15368', '15369', '15370', '15376', '15377', '15378', '15379', '15380', '15381', '15382', '15383',
    
    # Greene County
    '15310', '15311', '15312', '15313', '15314', '15315', '15316', '15317', '15320', '15321', '15322', '15323',
    '15324', '15325', '15327', '15329', '15330', '15331', '15332', '15333', '15334', '15335', '15336', '15337',
    '15338', '15339', '15340', '15341', '15342', '15343', '15344', '15345', '15346', '15347', '15348', '15349',
    '15350', '15351', '15352', '15353', '15354', '15355', '15356', '15357', '15358', '15359', '15360', '15361',
    '15362', '15363',
    
    # Fayette County
    '15401', '15410', '15411', '15412', '15413', '15415', '15416', '15417', '15419', '15420', '15421', '15422',
    '15423', '15424', '15425', '15427', '15428', '15429', '15430', '15431', '15432', '15433', '15434', '15435',
    '15436', '15437', '15438', '15439', '15440', '15441', '15442', '15443', '15444', '15445', '15446', '15447',
    '15448', '15449', '15450', '15451', '15452', '15453', '15454', '15455', '15456', '15458', '15459', '15460',
    '15461', '15462', '15463', '15464', '15465', '15466', '15467', '15468', '15469', '15470', '15472', '15473',
    '15474', '15475', '15476', '15477', '15478', '15479', '15480', '15482', '15483', '15484', '15485', '15486',
    '15487', '15488', '15489', '15490', '15491', '15492',
    
    # Westmoreland County
    '15601', '15605', '15606', '15610', '15611', '15612', '15613', '15615', '15616', '15617', '15618', '15619',
    '15620', '15621', '15622', '15623', '15624', '15625', '15626', '15627', '15628', '15629', '15630', '15631',
    '15632', '15633', '15634', '15635', '15636', '15637', '15638', '15639', '15640', '15641', '15642', '15644',
    '15646', '15647', '15648', '15650', '15651', '15652', '15653', '15654', '15655', '15656', '15657', '15658',
    '15660', '15661', '15662', '15663', '15664', '15665', '15666', '15667', '15668', '15670', '15671', '15672'
    ]

    # Filter the dataset to include only West Coast states
    df = df[df['State'].isin(states)]
     # Create a mask to filter the dataframe
    mask = df['Zip'].apply(lambda x: any(zip_code in str(x) for zip_code in zip))
    
    # Apply the mask to filter the dataframe
    df = df[mask]
    
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program
    
    # If we have data, continue with processing
    df = pel_process(df)
    
    return df