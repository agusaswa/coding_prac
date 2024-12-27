import markdown
import csv
from datetime import datetime

# Function to generate content for a page
def generate_page(name_1, name_2, title, company_logo, content, orientation="portrait"):
    """
    Generate a single HTML page with specified content and orientation.

    :param name_1: Designer's name.
    :param name_2: Checker’s name.
    :param title: Page title.
    :param company_logo: Path to the logo image.
    :param content: HTML content for the page.
    :param orientation: Page orientation ("portrait" or "landscape").
    :return: A string of the generated HTML for the page.
    """
    return f"""
    <div class="page-container {orientation}">
        <div class="header">
            <div class="details">
                <p>Designed by: {name_1}</p>
                <p>Checked by: {name_2}</p>
                <p>Title: {title}</p>
                <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
            <div class="logo">
                <img src="{company_logo}" alt="Company Logo">
            </div>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="empty-lines"></div>
    </div>
    <div class="page-break"></div>
    """

# Function to convert Markdown file to HTML
def convert_markdown_to_html(file_name):
    # Read the Markdown file
    with open(file_name, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    # Convert Markdown to HTML using the markdown library
    html_content = markdown.markdown(markdown_content)
    return html_content

# Function to convert CSV file to HTML
def convert_csv_to_html(file_name):
    # Read the CSV file
    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        csv_content = list(reader)
    
    # Start building the HTML table
    html_table = '<table class="data-table">'
    
    # Add table headers (from the first row of the CSV)
    html_table += '<tr>'
    for header in csv_content[0]:
        html_table += f'<th>{header}</th>'
    html_table += '</tr>'
    
    # Add the rest of the table rows
    for row in csv_content[1:]:
        html_table += '<tr>'
        for cell in row:
            html_table += f'<td>{cell}</td>'
        html_table += '</tr>'
    
    # Close the table
    html_table += '</table>'
    
    return html_table

# Function to add content to the correct page in pages_dict
def add_content_to_page(content_type, page_number, content, pages_dict):
    """
    Add content (markdown/csv) to the specific page in pages_dict.

    :param content_type: The type of content ("markdown" or "csv").
    :param page_number: The page number (1, 2, 3).
    :param content: The content to add (HTML converted markdown or CSV).
    :param pages_dict: The dictionary containing page details.
    """
    # Check if the page number exists in pages_dict
    if page_number in pages_dict:
        pages_dict[page_number][content_type] += content
    else:
        print(f"Page number {page_number} not found in pages_dict.")

# Example usage in your generate_html_report function
def generate_html_report(files_info, name_1, name_2, title, company_logo, pages_dict, suffix):
    # Process each file info
    for file_info in files_info:
        for file_type, file_data in file_info.items():
            file_name, page_number = file_data
            if file_type.startswith('md'):
                markdown_html = convert_markdown_to_html(file_name)
                add_content_to_page("markdown", page_number, markdown_html, pages_dict)
            elif file_type.startswith('csv'):
                csv_html = convert_csv_to_html(file_name)
                add_content_to_page("csv", page_number, csv_html, pages_dict)
    
    # Generate the HTML content for each page dynamically
    pages = ""
    for page_number in pages_dict:
        page_content = generate_page(
            name_1, 
            name_2, 
            title, 
            company_logo, 
            pages_dict[page_number]["markdown"] + pages_dict[page_number]["csv"],
            orientation=pages_dict[page_number].get("orientation", "portrait")  # Default to portrait if no orientation is provided
        )
        pages += page_content
    
    # Create final HTML content
    final_html = html_template.format(pages=pages)
    
    # Save to an HTML file
    with open(f"output_{suffix}.html", "w", encoding="utf-8") as file:
        file.write(final_html)
    print(f"HTML file generated: output_{suffix}.html")

def create_page(total_page, ori_key="P"):
    """
    Generate a dictionary for pages with the specified orientation for each page in the range.
    
    :param start_page: The starting page number.
    :param end_page: The ending page number.
    :param orientation: The orientation for all pages ("portrait" or "landscape").
    :return: A dictionary with page numbers as keys and corresponding orientation values.
    """
    # Initialize an empty dictionary
    pages_dict = {}
    orientation = {"P": "portrait", "L": "landscape"}
    
    # Loop through the range of page numbers and assign the specified orientation
    for page in range(1, total_page + 1):
        pages_dict[page] = {
            "markdown": "",
            "csv": "",
            "orientation": orientation[ori_key]
        }

    return pages_dict


# Define the template outside the function
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 0;
            background-color: white;
        }}
        .container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        .page-container {{
            margin: 0 auto;
            padding: 20px;
        }}
        .portrait {{
            width: 800px;
            height: auto;
            padding-right: 20px; /* Add padding to ensure content doesn't touch the right edge */
            margin: 0 auto;
        }}
        .landscape {{
            width: 100%;
            height: auto;
            padding-left: 40px; /* Add padding to ensure content doesn't touch the left edge */
            padding-right: 40px;
            box-sizing: border-box;
            margin: 0 auto;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #000;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .header .details {{
            font-size: 11px;
        }}
        .header .details p {{
            margin: 0;
        }}
        .header .logo {{
            text-align: right;
        }}
        .header .logo img {{
            height: 65px;
            width: auto;
        }}
        .content {{
            font-size: 11px;
            line-height: 1.6;
            color: #333;
        }}
        .content h1 {{
            font-size: 17px;
            margin-top: 0;
        }}
        .content h2 {{
            font-size: 15px;
            margin-top: 0;
        }}
        .content h3 {{
            font-size: 13px;
            margin-top: 0;
        }}
        .content h4 {{
            font-size: 12px;
            margin-top: 0;
        }}

        /* Updated table styles */
        .content .data-table {{
            width: auto;
            margin: 20px 0;
            font-size: 11px;
            text-align: left;
            overflow-x: auto;
            table-layout: fixed; /* Fixed table layout prevents auto column width adjustment */
            border-collapse: collapse; /* Ensures borders don't double up */
            max-width: 100%; /* Ensure table doesn't exceed the page width */
        }}

        /* Limit table width */
        .content .data-table th, .content .data-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            max-width: 80px; /* Limit column width */
            word-wrap: break-word; /* Prevents overflow */
        }}

        /* First row with light gray background */
        .content .data-table tr:first-child {{
            background-color: #f2f2f2; /* Light gray */
        }}

        /* Header row text alignment */
        .content .data-table th {{
            text-align: left;
            padding-right: 10px; /* Allow for a small space between header text and column edge */
        }}

        /* Optional: Row hover effect (screen only) */
        .content .data-table tr:not(:first-child):hover {{
            background-color: #f9f9f9; /* Slightly lighter background on hover */
        }}

        .page-break {{
            page-break-after: always;
        }}

        /* Print styling */
        @media print {{
            .container {{
                border: none;
            }}
            .content .data-table {{
                width: 100%; /* Ensure table fits well for print */
                border: none; /* Removes border box around the table */
                overflow-x: auto; /* Handle overflow on wide tables */
                table-layout: fixed; /* Keeps columns from expanding too much */
                border-collapse: collapse; /* Ensure borders don't double up */
            }}
            .content .data-table td, .content .data-table th {{
                border: 1px solid #ddd; /* Ensures internal borders for print */
                padding: 8px; /* Ensures consistent padding */
                background-color: transparent; /* Make sure background color is transparent */
            }}
            .content .data-table tr:first-child {{
                background-color: #f2f2f2; /* Ensures first row is light gray in print */
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {pages}
    </div>
</body>
</html>
"""