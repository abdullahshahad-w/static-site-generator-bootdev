from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("Text type is wrong, not in the enum")

    if text_node.text_type.name == "TEXT":
        return LeafNode(value=text_node.text)

    if text_node.text_type.name == "BOLD":
        return LeafNode(tag="b", value=text_node.text)

    if text_node.text_type.name == "ITALIC":
        return LeafNode(tag="i", value=text_node.text)

    if text_node.text_type.name == "CODE":
        return LeafNode(tag="code", value=text_node.text)

    if text_node.text_type.name == "LINK":
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    if text_node.text_type.name == "IMAGE":
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})