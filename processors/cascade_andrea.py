# processors/cascade_andrea.py
def process(df):
    """Process for Cascade - Andrea combination"""
    column_mapping = {
        'old_name1': 'new_name1',
        'old_name2': 'new_name2'
    }
    return df.rename(columns=column_mapping)