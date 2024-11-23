from nbconvert import HTMLExporter
import nbformat

def convert_notebook_to_html(input_notebook: str, output_html: str):
    # Load the notebook
    with open(input_notebook, 'r', encoding='utf-8') as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Create the HTML exporter
    html_exporter = HTMLExporter()

    # Convert the notebook to HTML
    body, resources = html_exporter.from_notebook_node(notebook_content)

    # Write the HTML output to a file
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(body)