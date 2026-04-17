import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is an image", TextType.IMAGE)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()