import re
from enum import Enum
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid Delimiter")
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                result.append(TextNode(part, TextType.TEXT))

            else:
                result.append(TextNode(part, text_type))

    return result


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    result = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        image_info = extract_markdown_images(node.text)

        if not image_info:
            result.append(node)
            continue

        original_text = node.text

        for image_alt, image_link in image_info:
            section = original_text.split(f"![{image_alt}]({image_link})", 1)

            if section[0] != "":
                result.append(TextNode(section[0], TextType.TEXT))

            result.append(TextNode(image_alt, TextType.IMAGE, image_link))

            original_text = section[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))

    return result


def split_nodes_link(old_nodes):
    result = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        link_info = extract_markdown_links(node.text)

        if not link_info:
            result.append(node)
            continue

        original_text = node.text

        for link_text, link_url in link_info:
            section = original_text.split(f"[{link_text}]({link_url})", 1)

            if section[0] != "":
                result.append(TextNode(section[0], TextType.TEXT))
                
            result.append(TextNode(link_text, TextType.LINK, link_url))

            original_text = section[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.TEXT))

    return result


def text_to_TextNode(markdown_text):
    node = TextNode(markdown_text, TextType.TEXT)

    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)

    images = split_nodes_image(code)

    return split_nodes_link(images)
        

def markdown_to_blocks(markdown_text):
    blocks = []

    parts = markdown_text.split("\n\n")

    for part in parts:
        if part.strip() == "":
            continue

        blocks.append(part.strip())

    return blocks


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_BlockType(block):
    from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):

    lines = block.split("\n")

    # HEADING
    first_line = lines[0]

    heading_count = 0

    for char in first_line:
        if char == "#":
            heading_count += 1
        else:
            break

    if (
        1 <= heading_count <= 6
        and len(first_line) > heading_count
        and first_line[heading_count] == " "
    ):
        return BlockType.HEADING

    # CODE
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # QUOTE
    is_quote = True

    for line in lines:
        if not line.startswith(">"):
            is_quote = False

    if is_quote:
        return BlockType.QUOTE

    # UNORDERED LIST
    is_unordered = True

    for line in lines:
        if not line.startswith("- "):
            is_unordered = False

    if is_unordered:
        return BlockType.UNORDERED_LIST

    # ORDERED LIST
    expected = 1
    is_ordered = True

    for line in lines:

        if not line.startswith(f"{expected}. "):
            is_ordered = False

        expected += 1

    if is_ordered:
        return BlockType.ORDERED_LIST

    # PARAGRAPH
    return BlockType.PARAGRAPH
