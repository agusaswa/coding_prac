import webbrowser
import os

def check(html_file: str) -> None:
    # Ensure the file exists before attempting to open it
    if os.path.exists(html_file):
        # Open the HTML file in the default browser
        webbrowser.open(f'file://{os.path.abspath(html_file)}')
    else:
        print(f"The file {html_file} does not exist.")