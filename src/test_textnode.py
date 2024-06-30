import unittest

from textnode import (
    TextNode, 
    text_type_text, 
    text_type_bold, 
    text_type_italic, 
    text_type_code, 
    text_type_image, 
    text_type_link)


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
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        self.assertEqual("TextNode(This is a text node, italic, https://www.boot.dev)", repr(node))

if __name__ == "__main__":
    unittest.main()