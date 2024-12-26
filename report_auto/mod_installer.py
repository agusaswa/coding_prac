import shutil
import os

directory = {
    "wind_des": "D:/Gede Agus Aswamada/Coding/wind_des"
}

def import_mod(src_folder, dest_folder=None):
    """
    Copies the contents of an external folder (src_folder) to the current working directory 
    or the specified destination folder (dest_folder).
    
    Args:
    - src_folder (str): The source folder path to copy from.
    - dest_folder (str, optional): The destination folder path to copy to. 
      Defaults to the current working directory if None.
    """
    
    # Use the current working directory if no destination is provided
    if dest_folder is None:
        dest_folder = os.getcwd()

    try:
        # Check if source folder exists
        if not os.path.exists(directory[src_folder]):
            raise FileNotFoundError(f"The source folder '{directory[src_folder]}' does not exist.")
        
        # Check if destination folder exists, create it if not
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        # Copy the entire folder
        shutil.copytree(directory[src_folder], os.path.join(dest_folder, os.path.basename(directory[src_folder])))
        print(f"Successfully imported '{directory[src_folder]}' to '{dest_folder}'")
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# copy_folder('path_to_external_folder')
