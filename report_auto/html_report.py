import markdown
import pandas as pd
from datetime import datetime

# Convert Markdown to HTML
def convert_markdown_to_html(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        md_content = file.read()
    return markdown.markdown(md_content)

# Read CSV and convert to HTML table
def convert_csv_to_html(csv_file):
    df = pd.read_csv(csv_file)
    return df.to_html(index=False)

# Define HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        @media print {{
            .container {{
                border: none; /* Hide border when printing */
            }}
            .empty-lines {{
                display: none; /* Hide empty lines when printing */
            }}
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
            font-size: 14px;
        }}
        .header .details .row {{
            display: flex;
            justify-content: space-between;
        }}
        .header .details p {{
            margin: 0;
        }}
        .header .logo {{
            text-align: right;
        }}
        .header .logo img {{
            height: 75px;
            width: auto;
        }}
        .content {{
            font-size: 14px;
            line-height: 1.6;
            color: #333;
        }}
        .content h2 {{
            font-size: 18px;
            margin-top: 0;
        }}
        .content p {{
            margin: 10px 0;
        }}
        .content .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .content .data-table th, .content .data-table td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        .content .data-table th {{
            background-color: #f4f4f4;
        }}
        .page-break {{
            page-break-after: always;
        }}
        .empty-lines {{
            height: 200px; /* Adjust this height for approximately 10 empty lines */
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

# Function to generate content for a page
def generate_page(name_1, name_2, title, company_logo, markdown_html, csv_html, date=None):
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    return f"""
    <div class="page">
        <div class="header">
            <div class="details">
                <p>Designed by: {name_1}</p>
                <p>Checked by: {name_2}</p>
                <div class="row">
                    <p>Title: {title}</p>
                    <p>Date: {date}</p>
                </div>
            </div>
            <div class="logo">
                <img src="{company_logo}" alt="Company Logo">
            </div>
        </div>
        <div class="content">
            {markdown_html}
            {csv_html}
        </div>
        <div class="empty-lines"></div>
        <div class="page-break"></div>
    </div>
    """

# Function to add content to specific pages
def add_content_to_page(content_type, page_number, content, pages_dict):
    if content_type == "markdown":
        pages_dict[page_number]["markdown"] = content
    elif content_type == "csv":
        pages_dict[page_number]["csv"] = content
    else:
        raise ValueError("Content type must be 'markdown' or 'csv'.")

# Main function to generate the report
def generate_html_report(files_info, name_1, name_2, title, company_logo):
    # Dictionary to hold content for each page (markdown and csv)
    pages_dict = {1: {"markdown": "", "csv": ""}, 2: {"markdown": "", "csv": ""}, 3: {"markdown": "", "csv": ""}}

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
    
    # Generate the HTML content for each page
    pages = ""
    for page_number in range(1, 4):
        page_content = generate_page(
            name_1, 
            name_2, 
            title, 
            company_logo, 
            pages_dict[page_number]["markdown"], 
            pages_dict[page_number]["csv"]
        )
        pages += page_content
    
    # Create final HTML content
    final_html = html_template.format(pages=pages)
    
    # Save to an HTML file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(final_html)
    print("HTML file generated: output.html")