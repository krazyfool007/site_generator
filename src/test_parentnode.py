import unittest

from htmlnode import HTMLNode,LeafNode,ParentNode

class TestParentNode(unittest.TestCase):
    def test_single_depth(self):
        node = ParentNode(tag="div", children=[LeafNode(tag="p", value="This is a paragraph."), LeafNode(tag="span", value="And this is a span.")])   
        expected_output = "<div><p>This is a paragraph.</p><span>And this is a span.</span></div>"
        self.assertEqual(node.to_html(), expected_output)

    def test_double_depth(self):
        node = ParentNode(tag="div", children=[LeafNode(tag="p", value="This is a paragraph."), LeafNode(tag="span", value="And this is a span."), ParentNode(tag="div", children=[LeafNode(tag="p", value="This is a nested paragraph."), LeafNode(tag="span", value="And this is a nested span.")])])   
        expected_output = "<div><p>This is a paragraph.</p><span>And this is a span.</span><div><p>This is a nested paragraph.</p><span>And this is a nested span.</span></div></div>"
        self.assertEqual(node.to_html(), expected_output)


if __name__ == "__main__":
    unittest.main()




