import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text, 
    text_type_bold, 
    text_type_italic, 
    text_type_code, 
    text_type_image, 
    text_type_link)


from htmlnode import LeafNode

from inline_markdown import (
    extract_markdown_links,
    extract_markdown_images
)


class TestTextNode(unittest.TestCase):
    # Test to see if TextNode objects are equal
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    # Test to see if TextNode objects text are not equal
    def test_not_eq(self):
        node = TextNode("This is a text broad", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    # Test to see if the TextNode objects text_types
    def test_not_eq2(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertNotEqual(node, node2)

    # Test to see if the TextNode objects URL
    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node ", text_type_italic, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node , italic, https://www.boot.dev)", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_invalid_text_type(self):    
        with self.assertRaises(Exception):
            node = TextNode("Test","PNG")
            text_node_to_html_node(node)
    
    def test_valid_text_conversion(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_valid_bold_conversion(self):
        node = TextNode("This is a text node", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_valid_italic_conversion(self):
        node = TextNode("This is a text node", text_type_italic)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
        
    def test_valid_image_conversion(self):
        node = TextNode("This is a text node", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.boot.dev", "alt":"This is a text node"})

if __name__ == "__main__":
    unittest.main()