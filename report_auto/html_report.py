import markdown
import pandas as pd
from datetime import datetime
import csv

# Define HTML template with improved table styling
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
            font-size: 14px;
            text-align: left;
        }}
        .content .data-table th, .content .data-table td {{
            border: 1px solid #000; /* Single-line border */
            padding: 8px;
        }}
        .content .data-table th {{
            background-color: #f4f4f4; /* Light gray header */
            font-weight: bold;
        }}
        .content .data-table td {{
            background-color: #fff; /* White cell background */
        }}
        .content .data-table tr:nth-child(even) td {{
            background-color: #f9f9f9; /* Alternate row color */
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
        {pages} <!-- Pages will be inserted here -->
        <div class="empty-lines"></div> <!-- Empty lines added only at the bottom -->
    </div>
</body>
</html>
"""

# Function to generate CSV table
def generate_csv_table(csv_data):
    if not csv_data:
        return ""
    header = csv_data[0]
    rows = csv_data[1:]

    # Build table rows
    header_html = "<tr>" + "".join(f"<th>{col}</th>" for col in header) + "</tr>"
    rows_html = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )

    # Return complete table
    return f"""
    <table class="data-table">
        {header_html}
        {rows_html}
    </table>
    """

# Function to generate a single page's HTML
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

# Function to generate the HTML report
def generate_html_report(files_info, name_1, name_2, title, company_logo):
    pages = ""
    for file_info in files_info:
        for file, info in file_info.items():
            file_type = file.split('.')[-1]
            filename = info[0]
            page = info[1]

            # Initialize markdown_html and csv_html to empty strings
            markdown_html = ""
            csv_html = ""

            # Read the content of markdown or csv file
            if file_type == 'md':
                with open(filename, 'r') as md_file:
                    markdown_content = md_file.read()
                    markdown_html = f"<h2>{filename}</h2><div>{markdown_content}</div>"
            elif file_type == 'csv':
                with open(filename, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_data = list(csv_reader)
                    csv_html = generate_csv_table(csv_data)

            # Generate page for the content
            pages += generate_page(name_1, name_2, title, company_logo, markdown_html, csv_html)

    # Create final HTML
    final_html = html_template.format(pages=pages)

    # Save to an HTML file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(final_html)
    print("HTML file generated: output.html")