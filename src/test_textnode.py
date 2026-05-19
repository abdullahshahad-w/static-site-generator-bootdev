import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is the text", TextType.TEXT)
        node2 = TextNode("This is the text", TextType.TEXT)

        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("Blah", TextType.BOLD)
        node2 = TextNode("fck jews", TextType.BOLD)

        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()