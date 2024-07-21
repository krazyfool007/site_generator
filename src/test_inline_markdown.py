import unittest

from textnode import (
    TextNode, 
text_type_text, 
text_type_bold, 
text_type_code, 
text_type_image, 
text_type_italic, 
text_type_link
)
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnode
    
)

class TestInlinemarkdown(unittest.TestCase):
    def test_single_delimiter_pair(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        results = split_nodes_delimiter([node], "`", text_type_code)
        expected_results = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ]
        self.assertEqual(results, expected_results)
    
    def test_multiple_delimiter_pairs(self):
        node = TextNode("This is text with one `code block` and then another `code block` inside", text_type_text)
        results = split_nodes_delimiter([node], "`", text_type_code)
        expected_results = [
            TextNode("This is text with one ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and then another ",text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" inside", text_type_text)
        ]
        self.assertEqual(results, expected_results)       
        
    def test_unmatched_delimiter(self):
        with self.assertRaises(Exception) as e:
            node = TextNode("Test `code block found",text_type_text)
            split_nodes_delimiter([node], "`", text_type_code)
        
        self.assertEqual(str(e.exception), "Invalid Markdown Syntax: Unmatched delimiter" )

    def test_bold_delimiter(self):
        node = TextNode("This node contains **BOLD** text", text_type_text)
        result = split_nodes_delimiter([node], "**", text_type_bold)
        expected_result = [
            TextNode("This node contains ", text_type_text),
            TextNode("BOLD", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual(result, expected_result)

    def test_compound_function(self):
        node = TextNode("This node contains **BOLD** and *italic* text", text_type_text)
        test1 = split_nodes_delimiter([node], "**", text_type_bold)
        result = split_nodes_delimiter(test1,"*", text_type_italic)
        expected_results = [
            TextNode("This node contains " , text_type_text),
            TextNode("BOLD", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text", text_type_text)

        ]
        self.assertEqual(result,expected_results)

class TestExtractMarkdownImages(unittest.TestCase):

    def test_extract_double_markdown_images(self):
        results = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected_results = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(results, expected_results)

    def test_no_valid_images(self):
        results = extract_markdown_images("This is text")
        expected_results = []
        self.assertEqual(results, expected_results)


class TestExtractMarkdownLinks(unittest.TestCase): 

    def test_extract_double_markdown_links(self):
        results = extract_markdown_links("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        expected_results = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(results, expected_results)

    def test_no_valid_links(self):
        results = extract_markdown_links("This is text")
        expected_results = []
        self.assertEqual(results, expected_results)

class TestSplitNodesImages(unittest.TestCase):
    
    def test_single_image_split(self):
        node = TextNode("This is text with an image ![to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_images([node])
        expected_results = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

    def test_images_only(self):
        node = TextNode("![to boot dev](https://www.boot.dev)  ![to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_images([node])
        expected_results = [
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

    def test_images_first(self):
        node = TextNode("![to boot dev](https://www.boot.dev) This is text with an image ![to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_images([node])
        expected_results = [
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode(" This is text with an image ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

class TestSplitNodesLinks(unittest.TestCase):
    
    def test_single_link_split(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_links([node])
        expected_results = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

    def test_links_only(self):
        node = TextNode("[to boot dev](https://www.boot.dev)  [to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_links([node])
        expected_results = [
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

    def test_links_first(self):
        node = TextNode("[to boot dev](https://www.boot.dev) This is text with a link [to boot dev](https://www.boot.dev)",text_type_text)
        results = split_nodes_links([node])
        expected_results = [
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev")
        ]
        self.assertEqual(results, expected_results)

class TestTextToTextNode(unittest.TestCase):
    
    def test_text_with_all_types(self):
        node = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        results = text_to_textnode(node)

        expected_results = [
    TextNode("This is ", text_type_text),
    TextNode("text", text_type_bold),
    TextNode(" with an ", text_type_text),
    TextNode("italic", text_type_italic),
    TextNode(" word and a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" and an ", text_type_text),
    TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", text_type_text),
    TextNode("link", text_type_link, "https://boot.dev"),
]
        self.assertEqual(results, expected_results)

    def test_text_no_markdown(self):
        node = "This is just some plain text"
        results = text_to_textnode(node)
        expected_results = [
            TextNode("This is just some plain text", text_type_text)
            ]
        self.assertEqual(results,expected_results)

    def test_text_bad_delimiter(self):
        node = "This text is in **BOLD did you know that?"
        with self.assertRaises(Exception) as e:
            text_to_textnode(node)




if __name__ == "__main__":
    unittest.main()