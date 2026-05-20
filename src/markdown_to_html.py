from markdown_to_textnode import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    text_to_TextNode,
)
from htmlnode import LeafNode, ParentNode, text_node_to_HTMLNode
from textnode import TextNode, TextType


def extract_title(markdown):
    """Return the text of the first markdown h1 line (single #). Strip # and outer whitespace."""
    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("#") and not stripped.startswith("##"):
            return stripped[1:].strip()
    raise ValueError("No h1 header found in markdown")


def text_to_children(text):
    """Convert inline markdown text to a list of HTMLNode children."""
    text_nodes = text_to_TextNode(text)
    children = []
    for text_node in text_nodes:
        child = text_node_to_HTMLNode(text_node)
        children.append(child)
    return children


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    text = block[level + 1:]
    children = text_to_children(text)
    tag = f"h{level}"
    return ParentNode(tag, children)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    text = block.replace("\n", " ")
    children = text_to_children(text)
    return ParentNode("p", children)


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if line.startswith(">"):
            quote_lines.append(line[2:])
        else:
            quote_lines.append(line)
    
    text = " ".join(quote_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    lines = block.split("\n")
    list_items = []
    for line in lines:
        text = line.split(". ", 1)[1]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    
    return ParentNode("ol", list_items)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    text = block[3:-3]
    if text.startswith("\n"):
        text = text[1:]
    
    code_node = LeafNode("code", text)
    return ParentNode("pre", [code_node])


def block_to_html_node(block):
    """Convert a markdown block to an HTMLNode based on its type."""
    block_type = block_to_block_type(block)
    
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    """Convert a full markdown document to a single parent HTMLNode."""
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    return ParentNode("div", children)
