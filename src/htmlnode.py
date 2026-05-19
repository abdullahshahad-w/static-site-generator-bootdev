from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_HTML(self):
        raise NotImplementedError
    
    def props_to_HTML(self):
        if not self.props:
            return ""
        
        result = ''

        for key, value in self.props.items():

            result += f' {key}="{value}"'

        return result
    
    def __repr__(self):
        return f'tag={self.tag}, value={self.value}, children={self.children}, props={self.props}'
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_HTML(self):
        if self.value is None:
            raise ValueError("Must provide a Value")
        
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_HTML()

        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'tag={self.tag}, value={self.value}, props={self.props}'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_HTML(self):
        if not self.tag:
            raise ValueError("Must provide a tag to ParentNode")
        
        if self.children is None:
            raise ValueError("Must provide Children to ParentNode")
        
        html_format = ""
        props = self.props_to_HTML()

        for child in self.children:
            html_format += child.to_HTML()

        return f'<{self.tag}{props}>{html_format}</{self.tag}>'
        

def text_node_to_HTMLNode(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("This shiih is not in TextType blud")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": f"{text_node.url}"})
    
    if text_node.text_type == TextType.IMAGE:
        props = {"src": f"{text_node.url}",
                 "alt": f"{text_node.text}"}
        
        return LeafNode("img", "", props=props)
    
