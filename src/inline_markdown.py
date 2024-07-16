from textnode import (
    TextNode, 
text_type_text, 
text_type_bold, 
text_type_code, 
text_type_image, 
text_type_italic, 
text_type_link
)

import re

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid Markdown Syntax: Unmatched delimiter")
            split_node = node.text.split(delimiter)
            for i in range(len(split_node)):
                if (split_node[i] != ""):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_node[i], text_type_text))
                    else:
                        new_nodes.append(TextNode(split_node[i], text_type))
                               
    return new_nodes

def extract_markdown_images(text: str) -> list:
    return re.findall(r"!+\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes: list) -> list:
    new_nodes = []
    
    
    for node in old_nodes:
        # Check the node for any images and store them in an array of tuples.
        images = extract_markdown_images(node.text)

        
        # If we don't find any images in the node, append it and move to the next node.
        if not images:
            new_nodes.append(node)
            continue

        sections = [node.text]
        
        # This next section takes in the text from the TextNode and splits it up based on the images found.
        for alt_text, url in images:
            new_sections = []
            for section in sections:
                split_results = section.split(f"![{alt_text}]({url})", 1)
                new_sections.extend(split_results)
            sections = new_sections

        # Convert split sections into TextNodes if they aren't empty, add any images as you go
        for section in sections:
            if section.strip():
                new_nodes.append(TextNode(section, text_type_text))
            
            if images:
                alt_text, url = images.pop(0)
                new_nodes.append(TextNode(alt_text, text_type_image, url))



    return new_nodes

def split_nodes_links(old_nodes):
    pass