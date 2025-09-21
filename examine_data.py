#!/usr/bin/env python3
import pandas as pd
import numpy as np

def examine_excel_data():
    """Examine the structure and content of the Excel file"""
    try:
        # Read the Excel file
        df = pd.read_excel('Stellest_Restrospective Data to Hindustan.xlsx')
        
        print("=== EXCEL DATA EXAMINATION ===")
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\n=== FIRST 5 ROWS ===")
        print(df.head())
        
        print("\n=== DATA TYPES ===")
        print(df.dtypes)
        
        print("\n=== MISSING VALUES ===")
        print(df.isnull().sum())
        
        print("\n=== BASIC STATISTICS ===")
        print(df.describe())
        
        print("\n=== UNIQUE VALUES IN CATEGORICAL COLUMNS ===")
        for col in df.columns:
            if df[col].dtype == 'object':
                print(f"{col}: {df[col].unique()}")
        
        # Save processed data info
        with open('data_analysis.txt', 'w') as f:
            f.write(f"Dataset shape: {df.shape}\n")
            f.write(f"Columns: {list(df.columns)}\n")
            f.write(f"Data types:\n{df.dtypes}\n")
            f.write(f"Missing values:\n{df.isnull().sum()}\n")
        
        return df
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

if __name__ == "__main__":
    df = examine_excel_data()
