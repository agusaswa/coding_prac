import html_report

name_1 = "GAA"
name_2 = "TYA"
title = "RC Beam Design Calculation"
company_logo = "Company Logo.JPG"  # Replace with the URL or path to your logo
files_info = [
    {"md_file_1": ["example1.md", 1], "md_file_2": ["example2.md", 3]},  # Markdown files and their page numbers
    {"csv_file_1": ["data1.csv", 2], "csv_file_2": ["data2.csv", 3]}       # CSV files and their page numbers
]

html_report.generate_html_report(files_info, name_1, name_2, title, company_logo)
