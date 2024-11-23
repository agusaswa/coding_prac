import pandas as pd
import datetime
import os

def export(df: pd.DataFrame, base_filename: str) -> None:
    # Get the current timestamp and format it as a string
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create the new filename by appending the timestamp to the base filename
    new_filename = f"{base_filename}_{timestamp}.csv"
    
    # Save the DataFrame to a CSV file with the new filename
    df.to_csv(new_filename, index=False)
    
    print(f"File saved as {new_filename}")

    # Read the saved file back into a DataFrame and return it
    df_new = pd.read_csv(new_filename)
    
    return df_new

def overwrite(df: pd.DataFrame, filename: str) -> None:
    # Overwrite the existing CSV file with the new DataFrame
    df.to_csv(filename, index=False)
    print(f"File {filename} has been overwritten.")
    
    # Read the saved file back into a DataFrame and return it
    df_new = pd.read_csv(filename)
    
    return df_new

def export_to_csv_by_range(excel_file: str, csv_file: str, row_range: range, col_range: range) -> None:
    
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file, engine ='openpyxl')
    
    # Select rows and columns based on the provided ranges
    selected_df = df.iloc[row_range, col_range]
    
    # Export the selected rows and columns to CSV
    selected_df.to_csv(csv_file, index=False)
    print(f"Data has been exported to {csv_file}")

def export_to_csv_by_name(excel_file: str, csv_file: str, row_labels: list, col_names: list) -> None:
    
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file, engine ='openpyxl')
    
    # Select rows and columns by name/label
    selected_df = df.loc[row_labels, col_names]
    
    # Export the selected rows and columns to CSV
    selected_df.to_csv(csv_file, index=False)
    print(f"Data has been exported to {csv_file}")

def export_to_csv_by_col_range(
    excel_file: str,
    csv_file: str,
    row_labels: list = None,  # List of row labels or indices to include
    col_range: tuple = None
    ) -> None:
    
    # Check if the file exists
    if not os.path.exists(excel_file):
        raise FileNotFoundError(f"Excel file not found: {excel_file}")

    # Read the Excel file
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Filter rows by labels or indices
    if row_labels is not None:
        df = df.loc[row_labels]

    # Filter columns by range (start and end positions)
    if col_range is not None:
        start, end = col_range
        df = df.iloc[:, start:end]

    # Save to CSV
    df.to_csv(csv_file, index=False)
    print(f"CSV file has been saved at: {csv_file}")

def export_to_csv_by_row_range(excel_file: str, csv_file: str, row_range: range, col_names: list) -> None:
    
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file, engine ='openpyxl')
    
    # Select rows and columns by name/label
    selected_df = df.loc[row_range, col_names]
    
    # Export the selected rows and columns to CSV
    selected_df.to_csv(csv_file, index=False)
    print(f"Data has been exported to {csv_file}")

# def main():
#     # Example usage
#     excel_file = 'new_2024-11-20_16-05-50.xlsx'  # Path to your input Excel file
#     csv_file = 'output_file5.csv'  # Path to your output CSV file
#     row_labels = [5,8,9]  # Specify row labels (indices or actual row labels depending on your file)
#     col_range = (0,5)  # Specify the column names to export

#     export_to_csv_by_col_range(excel_file, csv_file, row_labels,col_range)
#     return None

# if __name__ == '__main__':
#     main()

