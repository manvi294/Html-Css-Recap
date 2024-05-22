import pandas as pd

# Load the Excel file
file_path = 'path/to/your/excel_file.xlsx'
df = pd.read_excel(file_path)

# Define the mapping rules (in lowercase for case insensitivity)
status_mapping = {
    'new': 'Pre-Execution',
    'requested': 'Pre-Execution',
    'in progress': 'Execution',
    'waiting': 'Execution',
    'on hold': 'Execution'
}

# Function to apply the mapping
def map_status(status):
    if isinstance(status, str):
        return status_mapping.get(status.lower(), status)
    return status

# Apply the mapping to all columns that start with 'status' (case insensitive)
for col in df.columns:
    if col.lower().startswith('status'):
        df[col] = df[col].apply(map_status)

# Save the modified DataFrame back to an Excel file
output_file_path = 'path/to/your/output_excel_file.xlsx'
df.to_excel(output_file_path, index=False)

print(f"Data successfully modified and saved to {output_file_path}")
