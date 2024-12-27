import pandas as pd

def convert_excel_to_csv(excel_path, csv_filename, start_row=0, start_col='A', end_row=None, end_col=None):
    # Read the Excel file, ensuring no row is treated as an index
    excel_data = pd.read_excel(excel_path, engine='openpyxl', header=None, index_col=None)

    # If start_col is a letter, convert it to a column index (0-based index)
    if isinstance(start_col, str) and start_col.isalpha():
        start_col_idx = ord(start_col.upper()) - ord('A')  # Convert column 'A', 'B', etc. to index (0-based)
    else:
        start_col_idx = start_col

    # If end_col is provided, convert it similarly
    if isinstance(end_col, str) and end_col.isalpha():
        end_col_idx = ord(end_col.upper()) - ord('A') + 1  # Convert column 'A', 'B', etc. to index (0-based)
    else:
        end_col_idx = end_col

    # If end_row is None, set it to the number of rows in the data
    if end_row is None:
        end_row = len(excel_data)

    # Slice the data based on the start and end rows/columns
    excel_data = excel_data.iloc[start_row-1:end_row, start_col_idx:end_col_idx]

    # Reset the index to avoid the unwanted '1,2,3' index in the CSV file
    excel_data.reset_index(drop=True, inplace=True)

    # Convert to CSV without including the index
    excel_data.to_csv(csv_filename, index=False)  # Prevent writing index to CSV
    print(f"CSV file {csv_filename} has been created.")
