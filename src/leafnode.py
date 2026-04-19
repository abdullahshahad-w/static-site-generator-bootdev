from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNone must have a value")
        
        if self.tag is None:
            return self.value
        
        props_string = super().props_to_html()
        
        if props_string:
            return f'<{self.tag} {props_string}>{self.value}</{self.tag}>'
        
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"