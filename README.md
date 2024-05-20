import pandas as pd
import os
import glob

def merge_csv_files(folder_path, key='ticket ID'):
    # Get a list of all CSV files in the specified folder
    file_list = glob.glob(os.path.join(folder_path, '*.csv'))
    
    # Initialize an empty dataframe for the merged result
    merged_df = pd.DataFrame()
    
    for file in file_list:
        # Read the CSV file into a dataframe
        df = pd.read_csv(file)
        
        # Extract the file name without extension
        file_name = os.path.splitext(os.path.basename(file))[0]
        
        # Rename columns with the format <original field name>_<file name>
        df.rename(columns=lambda x: f"{x}_{file_name}" if x != key else x, inplace=True)
        
        # Merge dataframes on the key
        if merged_df.empty:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=key, how='outer')
    
    return merged_df

# Path to the folder containing the CSV files
folder_path = r'C:\path\to\your\folder'  # Replace with the actual path to your folder

# Merge the CSV files
merged_data = merge_csv_files(folder_path)

# Save the merged data to a new CSV file
merged_data.to_csv(os.path.join(folder_path, 'merged_output.csv'), index=False)
