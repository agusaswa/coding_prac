from playwright.async_api import async_playwright
import os

async def convert(html_files, orientations):
    """
    Convert HTML files to PDF with specified orientations.

    Args:
        html_files (list): List of HTML file paths.
        orientations (dict): Dictionary mapping file names to "portrait" or "landscape".
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        for html_file in html_files:
            page = await context.new_page()
            await page.goto(f'file://{os.path.abspath(html_file)}')

            # Inject custom CSS to enforce white background and fix table layout
            await page.add_style_tag(content="""
                @media print {{
                    body, html {{
                        background-colour: white !important;
                        color: black;
                    }}
                    * {{
                        background-colour: transparent !important;
                    }}

                    /* Ensure the table follows HTML layout */
                    .content .data-table {{
                        width: 100%; /* Ensure table width does not auto-expand beyond container */
                        table-layout: fixed; /* Ensure columns adjust based on content */
                        border-collapse: collapse; /* Ensure borders do not double up */
                    }}

                    /* Optional: Enforce column width constraints to avoid excessive stretching */
                    .content .data-table th, .content .data-table td {{
                        padding: 8px;
                        max-width: 80px; /* Set max width for columns */
                        word-wrap: break-word;
                        overflow: hidden; /* Prevent overly wide columns */
                    }}

                    .content .data-table tr:first-child {{
                        background-color: #f2f2f2; /* Light gray background for the first row */
                    }}
                    /* Ensure the page doesn't appear empty with a fallback element */
                    body:empty::before {{
                        content: "\00a0"; /* Adds a space if the body is empty */
                    }}
                }}
            """)

            # Determine the orientation for the current file
            file_name = os.path.basename(html_file)
            orientation = orientations.get(file_name, "portrait")

            # Set PDF options
            output_file = os.path.splitext(html_file)[0] + ".pdf"
            pdf_options = {
                "path": output_file,
                "format": "A4",
                "print_background": True,
                "landscape": orientation.lower() == "landscape",  # True for landscape, False for portrait
            }

            # Generate the PDF
            await page.pdf(**pdf_options)
            print(f"Converted {html_file} to {output_file} with {orientation} orientation.")

        await browser.close()


