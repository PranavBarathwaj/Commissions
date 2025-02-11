# processors/sps_john.py
def process(df):
    """Process for SPS - John combination"""
    df = df.drop_duplicates()
    df = df.rename(columns={"InvoiceNo": "Name"})
    # Add specific processing
    return df