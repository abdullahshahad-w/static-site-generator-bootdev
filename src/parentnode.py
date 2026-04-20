from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Must have a tag value")
        
        if self.children is None:
            raise ValueError("Must have children value")
        
        html_format = ""

        for child in self.children:
            html_format += child.to_html()

        props_string = super().props_to_html()

        if props_string:

            return f'<{self.tag} {props_string}>{html_format}</{self.tag}>'
        
        else:
            return f'<{self.tag}>{html_format}</{self.tag}>'