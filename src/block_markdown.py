import re

from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode
)

from textnode import (
    TextNode,
    text_node_to_html_node, 
    text_type_text, 
    text_type_bold, 
    text_type_code, 
    text_type_image, 
    text_type_italic, 
    text_type_link
)

from inline_markdown import (
    text_to_textnode
)

block_type_paragragh = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"

# Breaks raw markdown into a list of blocks
def markdown_to_blocks(markdown: str) -> list:
    # Initialized the blocks list with a starting value to avoid IndexError
    blocks = [""]

    # Loop through the raw markdown text line by line
    for line in markdown.split("\n"):

        # If you encounter a blank value it was an empty line and must be skipped
        if line == "":

            # New block added, starting value of "" to allow us to add an f-string to it.
            blocks.append("")
            continue

        # Using -1 ensures that we are always appending to the most recent block
        blocks[-1] += f"{line}\n"

        # Remove all whitespace from blocks
    blocks = [block.strip() for block in blocks if block.strip() != ""]

    return blocks

# Takes a block and returns the type of markdown content inside.
def block_to_block_type(block: str) -> str:
    lines = block.split("\n")
    
    #Code type test
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    
    if re.match(r"^#{1,6} ", block):
        return block_type_heading
    
    if all(line.startswith("> ") for line in lines):
        return block_type_quote
    
    if all(line.startswith(('*','-')) for line in lines):
        return block_type_unordered_list
    
    if all(re.match(r"^\d+. ", line) for line in lines):
        return block_type_ordered_list

    return block_type_paragragh


# Takes a full markdown document and converts it to HTMLNode
def markdown_to_html_node(markdown:str) -> HTMLNode:
    #Initilize html_nodes, we store the new HTMLNodes here
    block_nodes = []

    # Break the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    #Create a new HTMLNode based on the block type (Code, Heading, Quote, OL, IL or Paragraph)

    for block in blocks:
        block_type = block_to_block_type(block)

        #Match the block_type to the helper function to generate the correctly formated HTMLNode
        match block_type:
            # Quote Type Node
            case "quote":
                block_nodes.append(make_quote_node(block))

            # Code Type Node
            case "code":
                block_nodes.append(make_code_node(block))

            # Heading Type Node
            case "heading":
                block_nodes.append(make_heading_node(block))
            
            # Paragraph Type Node
            case "paragraph":
                block_nodes.append(make_paragraph_node(block))

            # Ordered List Type Node
            case "ordered list":
                block_nodes.append(make_ordered_list_node(block))
            
            # Unordered List Type Node
            case "unordered list":
                block_nodes.append(make_unordered_list_node(block))

            # Default case to catch invalid types
            case _:
                continue

    return ParentNode("div", block_nodes)

#Helper Functions for markdown_to_html_node

# Generates LeafNode children for the ParentNode
def generate_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnode(text)]

# Generates a quote ParentNode from provided block
def make_quote_node(block: str) -> ParentNode:
    stripped_block = '\n'.join([line[2:] for line in block.split("\n")])
    children = generate_children(stripped_block)
    node = ParentNode("blockquote",children)
    return node

# Generates a nested <pre> <code> ParentNode from provided block
def make_code_node(block:str) -> ParentNode:
    children = generate_children(block[2:-2])
    node = ParentNode("pre", [ParentNode("code",children)])
    return node


# Generates a Heading node based on number of #
def make_heading_node(block:str) -> ParentNode:
    # Check number of hash's to determine header level
    hash_count = len(block) - len(block.lstrip("#"))

    # Are there too few or too many?
    if hash_count < 1 or hash_count > 6:
        raise ValueError("Invalid heading level")
    
    children = generate_children(block.strip("#").strip())
    node = ParentNode(f"h{hash_count}", children)
    return node

# Generate a Paragraph Node
def make_paragraph_node(block:str) -> ParentNode:
    children = generate_children(block)
    node = ParentNode("p",children)
    return node

# Generate an unordered list node with correct nesting
def make_unordered_list_node(block:str) -> ParentNode:
    parents = []

    # Build a list of all the lines in the list, stripping the markdown characters and whitespace
    list_items = [line.lstrip("*- ").strip() for line in block.split("\n")]

    # Interate throw this list and generate ParentNode objects for each.
    for item in list_items:

        # Take the striped list item and generate the LeafNodes from the text
        parents.append(ParentNode("li",generate_children(item)))

    node = ParentNode("ul", parents)
    
    return node

# Generate an ordered list node with correct nesting
def make_ordered_list_node(block:str) -> ParentNode:
    parents = []

    # Build a list of all the lines in the list, stripping the markdown characters and whitespace
    list_items = [line[3:].strip() for line in block.split("\n")]

    # Interate throw this list and generate ParentNode objects for each.
    for item in list_items:

        # Take the striped list item and generate the LeafNodes from the text
        parents.append(ParentNode("li",generate_children(item)))

    node = ParentNode("ol", parents)
    
    return node