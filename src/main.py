from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    dummy = TextNode("This is text node", "bold", "https://www.boot.dev")
    print(dummy)
    print(text_node_to_html_node(dummy))
    pass

main()