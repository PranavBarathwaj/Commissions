# processors/pel_kyle.py
from .pel_common import process as pel_process
import sys
import streamlit as st

def process(df):
    """Shopify processing for John with additional customization"""
    # Define West Coast states
    states = ['PA', 'OH']
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
    '15660', '15661', '15662', '15663', '15664', '15665', '15666', '15667', '15668', '15670', '15671', '15672',

    # Trumbull County
    '44401', '44402', '44403', '44404', '44405', '44410', '44411', '44412', '44413', '44417', '44418', '44420',
    '44425', '44428', '44429', '44430', '44436', '44437', '44438', '44440', '44441', '44442', '44443', '44444',
    '44446', '44449', '44450', '44451', '44452', '44453', '44470', '44471', '44481', '44482', '44483', '44484',
    '44485', '44486', '44490', '44491', '44492',

    # Portage County
    '44201', '44202', '44211', '44214', '44215', '44224', '44231', '44240', '44241', '44242', '44243', '44255',
    '44260', '44265', '44266', '44272', '44274', '44275', '44278', '44288', '44411', '44429', '44446', '44460',
    '44470', '44485',

    # Summit County
    '44056', '44067', '44087', '44141', '44203', '44210', '44216', '44221', '44223', '44224', '44232', '44236',
    '44250', '44262', '44264', '44278', '44286', '44301', '44302', '44303', '44304', '44305', '44306', '44307',
    '44308', '44309', '44310', '44311', '44312', '44313', '44314', '44315', '44316', '44317', '44319', '44320',
    '44321', '44325', '44326', '44328', '44333', '44334', '44372', '44393', '44396', '44398', '44399',

    # Mahoning County
    '44401', '44402', '44403', '44405', '44406', '44408', '44409', '44410', '44411', '44412', '44413', '44415',
    '44416', '44417', '44418', '44420', '44422', '44423', '44425', '44427', '44429', '44430', '44431', '44432',
    '44436', '44440', '44441', '44442', '44443', '44444', '44445', '44446', '44449', '44450', '44451', '44452',
    '44453', '44454', '44455', '44471', '44472', '44473', '44490', '44493', '44501', '44502', '44503', '44504',
    '44505', '44506', '44507', '44509', '44510', '44511', '44512', '44513', '44514', '44515', '44555', '44601',
    '44609',

    # Stark County
    '44601', '44608', '44614', '44615', '44618', '44619', '44621', '44624', '44626', '44629', '44630', '44632',
    '44634', '44641', '44643', '44644', '44645', '44646', '44647', '44649', '44651', '44652', '44653', '44654',
    '44656', '44657', '44662', '44666', '44669', '44670', '44675', '44680', '44681', '44685', '44687', '44688',
    '44689', '44699', '44701', '44702', '44703', '44704', '44705', '44706', '44707', '44708', '44709', '44710',
    '44711', '44714', '44718', '44720', '44721', '44730', '44735', '44750', '44767', '44799',

    # Columbiana County
    '43920', '43930', '43932', '43938', '43939', '43940', '43941', '43942', '43943', '43945', '43948', '43950',
    '43951', '43952', '43953', '43961', '43962', '43963', '43964', '43968', '43971', '44401', '44408', '44413',
    '44415', '44422', '44423', '44424', '44425', '44427', '44431', '44432', '44441', '44442', '44443', '44445',
    '44455', '44460', '44490', '44609', '44625', '44634', '44640', '44644', '44657', '44665',

    # Jefferson County (OH)
    '43901', '43902', '43903', '43905', '43908', '43910', '43912', '43913', '43915', '43917', '43925', '43926',
    '43928', '43930', '43932', '43934', '43935', '43938', '43939', '43941', '43942', '43943', '43944', '43945',
    '43947', '43948', '43950', '43951', '43952', '43953', '43961', '43962', '43963', '43964', '43968', '43971',
    '43972', '43973', '43974', '43976', '43977', '43981', '43983', '43984', '43985', '43986', '43987', '43988',

    # Geauga County
    '44021', '44022', '44023', '44024', '44026', '44028', '44032', '44033', '44039', '44046', '44060', '44062',
    '44064', '44065', '44072', '44073', '44080', '44082', '44086', '44087', '44128', '44139', '44202', '44231',
    '44235', '44236', '44255', '44272', '44285', '44286',

    # Lake County
    '44003', '44010', '44024', '44026', '44030', '44032', '44033', '44039', '44041', '44045', '44047', '44048',
    '44057', '44060', '44061', '44062', '44064', '44065', '44070', '44072', '44073', '44076', '44077', '44080',
    '44081', '44082', '44084', '44085', '44086', '44087', '44088', '44089', '44092', '44093', '44094', '44095',
    '44096', '44097', '44099', '44124', '44143', '44256',

    # Medina County
    '44135', '44136', '44141', '44145', '44149', '44171', '44203', '44210', '44211', '44212', '44214', '44215',
    '44216', '44217', '44221', '44230', '44231', '44233', '44235', '44236', '44237', '44251', '44253', '44254',
    '44256', '44258', '44262', '44270', '44273', '44274', '44275', '44276', '44278', '44280', '44281', '44282',
    '44285', '44286', '44287', '44288', '44321',

    # Cuyahoga County
    '44001', '44004', '44011', '44012', '44013', '44014', '44017', '44021', '44022', '44040', '44047', '44070',
    '44101', '44102', '44103', '44104', '44105', '44106', '44107', '44108', '44109', '44110', '44111', '44112',
    '44113', '44114', '44115', '44116', '44117', '44118', '44119', '44120', '44121', '44122', '44123', '44124',
    '44125', '44126', '44127'
    ]

    # Filter the dataset to include only Ohio and specified ZIP codes
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