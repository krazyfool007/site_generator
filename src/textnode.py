from  htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url
        pass

    def __eq__(self, value: object) -> bool:
        return (
            self.text == value.text 
            and self.text_type == value.text_type 
            and self.url == value.url
            )
            
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):

    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text, None)
        case "bold":
            return LeafNode("b", text_node.text, None)
        case "italic":
            return LeafNode("i", text_node.text, None)
        case "code":
            return LeafNode("code", text_node.text, None)
        case "link":
            return LeafNode("a", text_node.text, {"href":f"{text_node.url}"})
        case "image":
            return LeafNode("img","",{"src":f"{text_node.url}", "alt":f"{text_node.text}"})
        case _: 
            raise Exception(f"Invalid Text Type: {text_node.text_type}")
