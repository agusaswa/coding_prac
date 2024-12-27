import re

# Define a function to replace placeholders
def replace_placeholders(file_path, replacements):
    # Read the markdown file
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the placeholders with corresponding values
    for placeholder, value in replacements.items():
        content = content.replace(f'{{{{{placeholder}}}}}', value)  # Double curly braces to match the placeholder format

    # Write the modified content back to the file or a new file
    with open('modified_md.md', 'w') as file:
        file.write(content)
    print(f"Placeholders replaced and saved to 'modified_md.md'.")