```import pandas as pd
import os
import json

def excel_to_json(excel_file_path):
    # Read the Excel file
    xls = pd.ExcelFile(excel_file_path)
    file_name = os.path.splitext(os.path.basename(excel_file_path))[0]
    
    # Loop through each sheet and save as JSON
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        json_data = df.to_json(orient='records')
        
        json_file_name = f"{file_name}_{sheet_name}.json"
        with open(json_file_name, 'w') as json_file:
            json_file.write(json_data)
            
        print(f"Sheet '{sheet_name}' written to {json_file_name}")

def main():
    # Example usage
    excel_file_path = 'path/to/your/excel/file.xlsx'
    excel_to_json(excel_file_path)

if __name__ == "__main__":
    main()
```