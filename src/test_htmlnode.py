import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_structure(self):
        dummy = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        
        node = HTMLNode(props=dummy)
        example =  'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), example)

    def test_eq(self):
        dummy = {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        
        node1 = HTMLNode("h", "Negro megro black Nigga",props=dummy)
        node2 = HTMLNode("h", "Negro megro black Nigga",props=dummy)

        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()