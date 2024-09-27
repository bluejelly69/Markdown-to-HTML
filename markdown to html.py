import re
import argparse
import logging
from typing import Dict, Callable

class MarkdownConverter:
    def __init__(self):
        self.conversion_rules: Dict[str, Callable] = {
            'headers': self._convert_headers,
            'bold': self._convert_bold,
            'italic': self._convert_italic,
            'links': self._convert_links,
            'lists': self._convert_lists,
            'code_blocks': self._convert_code_blocks,
            'blockquotes': self._convert_blockquotes,
            'horizontal_rules': self._convert_horizontal_rules,
            'paragraphs': self._convert_paragraphs,
        }

    def convert(self, markdown_text: str) -> str:
        """
        Convert Markdown text to HTML.
        """
        for rule in self.conversion_rules.values():
            markdown_text = rule(markdown_text)
        return markdown_text

    def _convert_headers(self, text: str) -> str:
        for i in range(6, 0, -1):
            pattern = r'^{} (.+)$'.format('#' * i)
            replacement = r'<h{}>\1</h{}>'.format(i, i)
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
        return text

    def _convert_bold(self, text: str) -> str:
        return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

    def _convert_italic(self, text: str) -> str:
        return re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    def _convert_links(self, text: str) -> str:
        return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

    def _convert_lists(self, text: str) -> str:
        # Unordered lists
        text = re.sub(r'^\s*[-*+]\s(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
        
        # Ordered lists
        text = re.sub(r'^\s*\d+\.\s(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'(<li>.*</li>)', r'<ol>\1</ol>', text, flags=re.DOTALL)
        
        return text

    def _convert_code_blocks(self, text: str) -> str:
        return re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)

    def _convert_blockquotes(self, text: str) -> str:
        text = re.sub(r'^>\s(.+)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)
        return re.sub(r'</blockquote>\s*<blockquote>', '\n', text)

    def _convert_horizontal_rules(self, text: str) -> str:
        return re.sub(r'^-{3,}$', r'<hr>', text, flags=re.MULTILINE)

    def _convert_paragraphs(self, text: str) -> str:
        text = re.sub(r'^\s*$', '</p><p>', text, flags=re.MULTILINE)
        return '<p>' + text + '</p>'

def convert_file(input_file: str, output_file: str):
    """
    Convert a Markdown file to HTML and save the result.
    """
    try:
        with open(input_file, 'r') as f:
            markdown_content = f.read()
        
        converter = MarkdownConverter()
        html_content = converter.convert(markdown_content)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        logging.info(f"Conversion successful. HTML file saved as {output_file}")
    except FileNotFoundError:
        logging.error(f"Error: The file {input_file} was not found.")
    except IOError:
        logging.error("An error occurred while reading or writing the file.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML")
    parser.add_argument("input_file", help="Path to the input Markdown file")
    parser.add_argument("output_file", help="Path for the output HTML file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    convert_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()