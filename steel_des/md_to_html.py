import pypandoc

# Define the input and output files
input_file = 'sectclass_report.md'
output_file = 'output.html'

# Convert Markdown to HTML using pypandoc
output = pypandoc.convert_file(input_file, 'html', outputfile=output_file, extra_args=['--mathjax', '-s'])

print(f"Converted {input_file} to {output_file}")
