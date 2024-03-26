from fastapi import HTTPException

import random
import pandas as pd

def generate_unique_id():
    return random.randint(100000, 999999)

def parse_excel_or_csv(file):
    # Define custom converter function to keep lists as lists
    def convert_to_list(x):
        try:
            # If it's a list (evaluates successfully), return it unchanged
            return eval(x)
        except:
            # If not, return the original value
            return x

    # Check if the file is CSV or XLSX
    if file.filename.endswith('.csv'):
        # If it's a CSV file, read it using pandas with custom converters
        df = pd.read_csv(file.file, converters={'current_location': convert_to_list})
    elif file.filename.endswith(('.xlsx', '.xls')):
        # If it's an Excel file, read it using pandas
        df = pd.read_excel(file.file)
        if 'current_location' in df.columns:
            df['current_location'] = df['current_location'].apply(eval)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")
    return df

technicial_skill_set = ["router setup", "cable repair", "software troubleshooting", "fiber optics", "customer service"]