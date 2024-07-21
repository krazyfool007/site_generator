import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    make_quote_node,
    make_code_node,
    make_heading_node,
    make_paragraph_node,
    make_unordered_list_node,
    make_ordered_list_node,
    block_type_paragragh,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)

from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode
)

class TestMarkdownToBlock(unittest.TestCase):
    def test_block_split(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        results = markdown_to_blocks(markdown)
        expected_results = ['# This is a heading',
                             'This is a paragraph of text. It has some **bold** and *italic* words inside',
                             '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
                             ]
        self.assertEqual(results, expected_results)

    def test_multiple_empty_lines(self):
        results = markdown_to_blocks("# Heading\n\n\nParagraph text here.\n\n\n* Item 1\n* Item 2\n* Item 3\n")
        expected_results = [
            '# Heading',
              'Paragraph text here.',
                '* Item 1\n* Item 2\n* Item 3'
                ]
        self.assertEqual(results, expected_results)

class TestBlockToBlockType(unittest.TestCase):
    def test_ordered_list_block(self):
        markdown = "1. First item\n2. Second item"
        results = block_to_block_type(markdown)
        expected_results = block_type_ordered_list
        self.assertEqual(results,expected_results)

    def test_quote_block(self):
        markdown = "> Quote number 1\n> Quote number 2\n> Quote number 3"
        results = block_to_block_type(markdown)
        expected_results = block_type_quote
        self.assertEqual(results, expected_results)

    def test_unordered_list_block(self):
        markdown = "- Bullet point one\n* Bullet point two"
        results = block_to_block_type(markdown)
        expected_results = block_type_unordered_list
        self.assertEqual(results,expected_results)

    def test_paragraph_block(self):
        markdown = "This is a single paragraph\nwith multiple lines."
        results = block_to_block_type(markdown)
        expected_results = block_type_paragragh
        self.assertEqual(results,expected_results)

    def test_ordered_code_block(self):
        markdown = "```Code block\n# Heading inside code block\n```"
        results = block_to_block_type(markdown)
        expected_results = block_type_code
        self.assertEqual(results,expected_results)

    def test_ordered_heading_block(self):
        markdown = "# Heading 1"
        results = block_to_block_type(markdown)
        expected_results = block_type_heading
        self.assertEqual(results,expected_results)

    def test_full_block_test(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        blocks = markdown_to_blocks(markdown)
        results = [block_to_block_type(block) for block in blocks]
        expected_results = [block_type_heading, block_type_paragragh, block_type_unordered_list]
        self.assertEqual(results,expected_results)

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_simple_markdown_test(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        results = markdown_to_html_node(markdown)
        
        expected_results = ParentNode("div",[
            ParentNode("h1",[
                LeafNode(None,"This is a heading")
            ]),
            ParentNode("p",[
                LeafNode(None,"This is a paragraph of text. It has some "),
                LeafNode("b", "bold"),
                LeafNode(None," and "),
                LeafNode("i", "italic"),
                LeafNode(None, " words inside")
            ]),
            ParentNode("ul",[
                ParentNode('li', [LeafNode(None,"This is the first list item in a list block")]),
                ParentNode('li', [LeafNode(None,"This is a list item")]),
                ParentNode('li', [LeafNode(None,"This is another list item")])
            ])
        ])
        self.assertEqual(results, expected_results)

class TestMarkdownToHTMLNodeHelpers(unittest.TestCase):
    def test_make_code_node(self):
        markdown = "```Code block\n# Heading inside code block\n```"
        results = make_code_node(markdown)
        expected_results = ParentNode("pre",[ParentNode("code", [LeafNode("code","Code block\n# Heading inside code block\n")])])
        self.assertEqual(results, expected_results)

    def test_make_quote_node(self):
        markdown = "> Quote number 1\n> Quote number 2\n> Quote number 3"
        results = make_quote_node(markdown)
        expected_results = ParentNode("blockquote", [LeafNode(None,"Quote number 1\nQuote number 2\nQuote number 3")])
        self.assertEqual(results, expected_results)

    def test_make_heading(self):
        markdown = "### Heading 3"
        results = make_heading_node(markdown)
        expected_results = ParentNode("h3", [LeafNode(None, "Heading 3")])
        self.assertEqual(results, expected_results)

    def test_make_paragraph(self):
        markdown = "This is a paragraph of text. It has some **bold** and *italic* words inside"
        results = make_paragraph_node(markdown)
        expected_results = ParentNode("p", [
            LeafNode(None, "This is a paragraph of text. It has some "), 
            LeafNode("b", "bold"), 
            LeafNode(None, " and "), 
            LeafNode('i', "italic"), 
            LeafNode(None," words inside")])
        self.assertEqual(results,expected_results)

    def test_make_unordered_list(self):
        markdown = "- Bullet point one\n* Bullet point two"
        results = make_unordered_list_node(markdown)
        expected_results = ParentNode("ul",[
            ParentNode('li', [
                LeafNode(None, "Bullet point one")
            ]),
            ParentNode('li', [
                LeafNode(None, "Bullet point two")
            ])
        ])
        self.assertEqual(results, expected_results)

    def test_make_ordered_list(self):
        markdown = "1. Bullet point one\n2. Bullet point two"
        results = make_ordered_list_node(markdown)
        expected_results = ParentNode("ol",[
            ParentNode('li', [
                LeafNode(None, "Bullet point one")
            ]),
            ParentNode('li', [
                LeafNode(None, "Bullet point two")
            ])
        ])
        self.assertEqual(results, expected_results)


if __name__ == "__main__":
    unittest.main()