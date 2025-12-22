import markdown
import pdfkit

def markdown_to_pdf(input_markdown_file, output_pdf_file):
    # Read the Markdown file
    with open(input_markdown_file, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)
    
    # Convert HTML to PDF
    pdfkit.from_string(html_content, output_pdf_file)
    print(f"PDF file created: {output_pdf_file}")

# Example usage
input_markdown = "example.md"  # Replace with your Markdown file
output_pdf = "output.pdf"      # Replace with your desired PDF file name
markdown_to_pdf(input_markdown, output_pdf)