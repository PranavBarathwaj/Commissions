# processors/pel_kyle.py
from .pel_common import process as pel_process
import sys
import streamlit as st

def process(df):
    """Shopify processing for John with additional customization"""
    
    states = ['MD', 'VA', 'DC']
    zip= [
    # Prince George's County (MD)
    '20601', '20607', '20608', '20613', '20623', '20705', '20706', '20707', '20708', '20710', 
    '20712', '20715', '20716', '20720', '20721', '20722', '20735', '20737', '20740', '20742', 
    '20743', '20744', '20745', '20746', '20747', '20748', '20762', '20769', '20770', '20772', 
    '20774', '20781', '20782', '20783', '20784', '20785',
    
    # Montgomery County (MD)
    '20812', '20814', '20815', '20816', '20817', '20818', '20832', '20833', '20837', '20841', 
    '20842', '20850', '20851', '20852', '20853', '20854', '20855', '20860', '20861', '20862', 
    '20866', '20868', '20871', '20872', '20874', '20876', '20877', '20878', '20879', '20880', 
    '20882', '20883', '20884', '20885', '20886', '20889', '20891', '20895', '20896', '20899', 
    '20901', '20902', '20903', '20904', '20905', '20906', '20907', '20908', '20910', '20911', 
    '20912', '20913',
    
    # Howard County (MD)
    '20701', '20723', '20763', '20777', '20794', '21029', '21036', '21042', '21043', '21044', 
    '21045', '21046', '21075', '21150',
    
    # Baltimore County (MD)
    '21013', '21020', '21022', '21023', '21027', '21030', '21031', '21051', '21053', '21057', 
    '21071', '21087', '21093', '21111', '21117', '21120', '21128', '21133', '21139', '21152', 
    '21155', '21156', '21162', '21163', '21204', '21206', '21207', '21208', '21212', '21219', 
    '21220', '21221', '21222', '21227', '21228', '21234', '21236', '21237', '21244', '21252', 
    '21282', '21286',
    
    # Baltimore City (MD)
    '21201', '21202', '21203', '21205', '21209', '21210', '21211', '21213', '21214', '21215', 
    '21216', '21217', '21218', '21223', '21224', '21225', '21226', '21229', '21230', '21231', 
    '21233', '21235', '21239', '21240', '21241', '21250', '21251', '21263', '21264', '21265', 
    '21270', '21273', '21274', '21275', '21278', '21279', '21280', '21281', '21283', '21287', 
    '21288', '21289', '21290', '21297', '21298',
    
    # Anne Arundel County (MD)
    '20711', '20724', '20733', '20755', '20758', '20764', '20765', '20776', '20778', '20779', 
    '21012', '21032', '21035', '21037', '21054', '21056', '21060', '21061', '21076', '21077', 
    '21090', '21108', '21113', '21114', '21122', '21140', '21144', '21146', '21225', '21226', 
    '21401', '21402', '21403', '21404', '21405', '21409',

    # Fairfax County (VA)
    '20120', '20121', '20122', '20124', '20151', '20153', '20170', '20171', '20172', '20190', 
    '20191', '20194', '22003', '22009', '22015', '22027', '22030', '22031', '22032', '22033', 
    '22034', '22035', '22036', '22039', '22041', '22042', '22043', '22044', '22046', '22060', 
    '22066', '22067', '22079', '22081', '22082', '22095', '22096', '22101', '22102', '22103', 
    '22106', '22107', '22108', '22109', '22116', '22118', '22119', '22121', '22122', '22124', 
    '22150', '22151', '22152', '22153', '22156', '22158', '22159', '22160', '22161', '22172', 
    '22180', '22181', '22182', '22183', '22184', '22185', '22199',
    
    # Hanover County (VA)
    '23005', '23015', '23047', '23059', '23069', '23102', '23111', '23116', '23146', '23162', 
    '23192',
    
    # Henrico County (VA)
    '23058', '23059', '23060', '23075', '23150', '23227', '23228', '23229', '23230', '23231', 
    '23233', '23238', '23242', '23255', '23273', '23294',
    
    # Falls Church (VA)
    '22040', '22042', '22043', '22044', '22046',
    
    # Arlington County (VA)
    '22201', '22202', '22203', '22204', '22205', '22206', '22207', '22209', '22210', '22211', 
    '22212', '22213', '22214', '22215', '22216', '22217', '22218', '22219', '22222', '22223', 
    '22225', '22226', '22227', '22229', '22230', '22234', '22240', '22241', '22242', '22243', 
    '22244', '22245', '22246',
    
    # Alexandria (VA)
    '22301', '22302', '22303', '22304', '22305', '22306', '22307', '22308', '22309', '22310', 
    '22311', '22312', '22313', '22314', '22315', '22320', '22321', '22323', '22331', '22332', 
    '22333', '22334', '22350',

    # District of Columbia (DC)
    '20001', '20002', '20003', '20004', '20005', '20006', '20007', '20008', '20009', '20010', 
    '20011', '20012', '20013', '20015', '20016', '20017', '20018', '20019', '20020', '20022', 
    '20023', '20024', '20026', '20027', '20029', '20030', '20032', '20033', '20035', '20036', 
    '20037', '20038', '20039', '20040', '20041', '20042', '20043', '20044', '20045', '20046', 
    '20047', '20049', '20050', '20051', '20052', '20053', '20055', '20056', '20057', '20058', 
    '20059', '20060', '20061', '20062', '20063', '20064', '20065', '20066', '20067', '20068', 
    '20069', '20070', '20071', '20073', '20074', '20075', '20076', '20077', '20078', '20080', 
    '20081', '20082', '20088', '20090', '20091', '20097', '20098', '20099'
    ]

    # Filter the dataset to include only West Coast states
    df = df[df['State'].isin(states)]
    df = df[df['Zip'].isin(zip)]
    # Check if the filtered DataFrame is empty
    if df.empty:
        st.warning(f"No entries found for states: {', '.join(states)}.")
        sys.exit()  # This will terminate the program
    
    # If we have data, continue with processing
    df = pel_process(df)
    
    return df