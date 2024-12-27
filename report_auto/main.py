# import html_report, html_to_pdf
# import asyncio
# import md_modify as mod

# replacements = {
#     'dead_load': str(1000),
#     'live_load': str(500)
# }

# # Specify the Markdown file path
# file_path = 'example1.md'

# # Call the function to replace placeholders
# mod.replace_placeholders(file_path, replacements)

# name_1 = "GAA"
# name_2 = "TYA"
# title = "RC Beam Design Calculation"
# company_logo = "Company Logo.JPG"  # Replace with the URL or path to your logo
# files_info = [
#     {
#         "md_file_1": ["example1.md", 1],
#     },
#     {
#         "md_file_2": ["example2.md", 2],
#         "csv_file_2": ["data2.csv", 2],
#     },
#     {
#         "md_file_3": ["modified_md.md", 3],
#         "csv_file_3": ["data1.csv", 3]
#     }
# ]

# # Define pages_dict outside the function
# pages_dict_1 = html_report.create_page(4,"L")
# pages_dict_2 = html_report.create_page(3,"P")
# html_report.generate_html_report(files_info, name_1, name_2, title, company_logo, pages_dict_1,1)
# html_report.generate_html_report(files_info, name_1, name_2, title, company_logo, pages_dict_2,2)

# # Example usage
# html_files = ["output_1.html", 
#               "output_2.html"]
# orientations = {
#     "output_1.html": "landscape", 
#     "output_2.html": "portrait",
# }
# asyncio.run(html_to_pdf.convert(html_files,orientations))

import excel_to_csv as xl

excel_path = r"D:\Gede Agus Aswamada\Coding\report_auto\data_xl_1.xlsx"
csv_filename = "trial_data_1.csv"
start_row = 5
start_col = "B"
xl.convert_excel_to_csv(excel_path, csv_filename, start_row, start_col,end_col="C")

