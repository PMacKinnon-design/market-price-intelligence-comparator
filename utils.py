
import pandas as pd
import os

def parse_uploaded_file(uploaded_file):
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
    if file_ext == ".csv":
        df = pd.read_csv(uploaded_file)
    elif file_ext in [".xls", ".xlsx"]:
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type")
    return df
