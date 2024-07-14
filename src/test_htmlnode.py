import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node,node2)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),  " href='https://www.google.com' target='_blank'")
        
    def test_repr(self):
        node = HTMLNode()
        #print(node)

    
if __name__ == "__main__":
    unittest.main()