import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter

class TestSplitNode(unittest.TestCase):
    def test_for_CODE(self):
        node = TextNode("Eiyoo wagwan `this is a code` word", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "`", TextType.CODE)

        ref_node = [
            TextNode("Eiyoo wagwan ", TextType.TEXT),
            TextNode("this is a code", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(node_list, ref_node)



    def test_for_ITALIC(self):
        node = TextNode("Eiyoo wagwan _this is a code_ word", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "_", TextType.ITALIC)

        ref_node = [
            TextNode("Eiyoo wagwan ", TextType.TEXT),
            TextNode("this is a code", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(node_list, ref_node)

    def test_for_BOLD(self):
        node = TextNode("Eiyoo wagwan **this is a code** word", TextType.TEXT)
        node_list = split_nodes_delimiter([node], "**", TextType.BOLD)

        ref_node = [
            TextNode("Eiyoo wagwan ", TextType.TEXT),
            TextNode("this is a code", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(node_list, ref_node)

    def test_no_delimeter(self):
        with self.assertRaises(ValueError):
            node = TextNode("Eiyoo wagwan this is a code word", TextType.TEXT)
            node_list = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_unclosed_delimiter(self):
        with self.assertRaises(ValueError):
            node = TextNode("Eiyoo wagwan **this is a code word", TextType.TEXT)
            node_list = split_nodes_delimiter([node], "**", TextType.BOLD)



if __name__ == "__main__":
    unittest.main()