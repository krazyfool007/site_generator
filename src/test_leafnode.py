import unittest

from htmlnode import HTMLNode,LeafNode

class TestLeafNode(unittest.TestCase):

    def test_eq(self):
        node = LeafNode(props={"href": "https://www.google.com", "target": "_blank"})
        node2 = LeafNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node,node2)

    def test_props_to_html(self):
        node = LeafNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),  " href='https://www.google.com' target='_blank'")
        
    def test_repr(self):
        node = LeafNode("p","This is my paragraph!")
        self.assertEqual(repr(node), "LeafNode(Tag: p, Value: This is my paragraph!, Props: None)")

    def test_no_tag(self):
        node = LeafNode(None, "This is my paragraph!")
        self.assertEqual(node.to_html(),"This is my paragraph!")
    
    def test_no_value(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode("p", None)
            leaf.to_html()
