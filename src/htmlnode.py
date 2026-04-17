class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children # list of HTMLNode
        self.props = props # a dict of key value pairs that contains attributes

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None or not self.props:
            return ""
        
        return " ".join(f'{k}="{v}"' for k, v in self.props.items())
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    