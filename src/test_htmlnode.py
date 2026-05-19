import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_HTMLNode
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):

    def test_props_to_HTML(self):
        props = {"href": "siuuuu.com",
                 "jew": "heres the coin"}
        
        node = HTMLNode("p", props=props)

        reference_str = ' href="siuuuu.com" jew="heres the coin"'

        self.assertEqual(reference_str, node.props_to_HTML())

    def test_props_to_HTML_none(self):
        node = HTMLNode("t1")

        ref_str = ""

        self.assertEqual(node.props_to_HTML(), ref_str)

    def test_props_to_HTML_empty(self):
        node = HTMLNode("p", props={})

        ref_str = ""

        self.assertEqual(node.props_to_HTML(), ref_str)

    def test_leaf_to_HTML_p(self):
        node = LeafNode("p", "Hello, World")

        self.assertEqual(node.to_HTML(), '<p>Hello, World</p>')

    def test_leaf_to_HTML_no_tag(self):
        node = LeafNode(None,value="nigga nigga nigga")

        ref_str = "nigga nigga nigga"

        self.assertEqual(node.to_HTML(), ref_str)

    def test_to_HTML_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_HTML(), "<div><span>child</span></div>")

    def test_to_HTML_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_HTML(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("a cat", TextType.IMAGE, "https://example.com/cat.png")
        html_node = text_node_to_HTMLNode(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/cat.png", "alt": "a cat"})

    def test_invalid_type(self):
        node = TextNode("some text", TextType.TEXT)
        node.text_type = "not_a_valid_type"
        with self.assertRaises(Exception):
            text_node_to_HTMLNode(node)

if __name__ == "__main__":
    unittest.main()