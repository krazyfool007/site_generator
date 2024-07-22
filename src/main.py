from textnode import TextNode, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import (
    markdown_to_html_node,
    extract_title
)


import os
import shutil


def main():

    if os.path.exists("/home/harry/site_generator/public"):
        shutil.rmtree("/home/harry/site_generator/public")

    copy_all_contents("/home/harry/site_generator/static", "/home/harry/site_generator/public")
    generate_pages_recursive("/home/harry/site_generator/content", "/home/harry/site_generator/template.html", "/home/harry/site_generator/public")

    pass

def copy_all_contents(source_path:str, destination_path):

    if not os.path.exists(source_path):
        raise ValueError("Source path doesn't exist")
    
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for file in os.listdir(source_path):
        if os.path.isdir(os.path.join(source_path,file)):
            print(f"Directory Found: {file}.")
            os.mkdir(os.path.join(destination_path,file))
            copy_all_contents(os.path.join(source_path,file), os.path.join(destination_path,file))
        else:
            print(os.path.join(destination_path,file))
            shutil.copy(os.path.join(source_path,file), os.path.join(destination_path,file))

    return

def generate_page(from_path, template_path, dest_path):

    if not os.path.exists(from_path):
        raise Exception("Invalid from_path")
    
    if not os.path.exists(template_path):
        raise Exception("Invalid template_path")
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as reader:
        markdown = reader.read()

    with open(template_path, "r") as reader:
        template = reader.read()

    html_string = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    
    print(dest_path)
    with open(dest_path, "x") as writer:
        writer.write(template)

    pass
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    print(f"Generating pages recursively:\nCurrent content path is: {dir_path_content} Current destination path is: {dest_dir_path}")

    for file in os.listdir(dir_path_content):
        if os.path.isdir(os.path.join(dir_path_content,file)):
            os.mkdir(os.path.join(dest_dir_path,file))
            generate_pages_recursive(os.path.join(dir_path_content,file), template_path, os.path.join(dest_dir_path,file))
        else:
            print(f"Generating page {file} from the content folder {dir_path_content}")
            generate_page(os.path.join(dir_path_content,file), template_path, os.path.join(dest_dir_path,file.replace(".md", ".html")))
        

    pass
    
main()