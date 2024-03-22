# Third Party
from bs4 import BeautifulSoup


# Main Section
def extract_content_summary(content):
    soup = BeautifulSoup(content, features='html.parser')

    block_tag_list = ["div", "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "blockquote", "pre", "table", "header", "footer", "section", "article", "nav", "aside", "address", "form", "fieldset", "hr"]

    # Extract style, script Tags
    for extract_tag in soup.find_all(['style', 'script']):
        extract_tag.extract()

    # Find all block tags
    block_tag_elements = soup.find_all(block_tag_list)
    for element in block_tag_elements:
        element = element.find(text=True, recursive=False)

        # Check if the block tag has text and not empty
        if element and not element.isspace():
            text = element.get_text()
            element.replace_with(text + '<br>')

    # Combine the text
    text_parts = soup.find_all(text=True)
    text_parts_filtered = filter(lambda text_part: len(text_part.strip()) >= 1, text_parts)
    content_summary = ' '.join(text_parts_filtered)

    # Strip last <br> tag
    content_summary = content_summary.rstrip('<br>')
    return content_summary
