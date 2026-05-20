import unittest
from textnode import TextNode, TextType
from markdown_to_textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_TextNode, markdown_to_blocks, block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is the text", TextType.TEXT)
        node2 = TextNode("This is the text", TextType.TEXT)

        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("Blah", TextType.BOLD)
        node2 = TextNode("fck jews", TextType.BOLD)

        self.assertNotEqual(node1, node2)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_bold_sections(self):
        node = TextNode("A **bold** and another **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("Plain text, no delimiters here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text, no delimiters here", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("Has `code` inside", TextType.TEXT),
            TextNode("untouched italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside", TextType.TEXT),
            TextNode("untouched italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # If you skip empty strings, drop the first TextNode("", TEXT) below.
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is `broken markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # Images: multiple images in one string
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![cat](https://example.com/cat.png) and ![dog](https://example.com/dog.png)"
        )
        self.assertListEqual(
            [
                ("cat", "https://example.com/cat.png"),
                ("dog", "https://example.com/dog.png"),
            ],
            matches,
        )

    # Images: no images present
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images at all.")
        self.assertListEqual([], matches)

    # Links: no links present
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("Just plain text here.")
        self.assertListEqual([], matches)

    # Links: image syntax should NOT be captured as a link
    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
            "An image ![alt text](https://example.com/img.png) should not appear."
        )
        self.assertListEqual([], matches)

    # Links: empty alt text
    def test_extract_markdown_links_empty_anchor(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    # Images: empty alt text
    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # split_nodes_image tests
    def test_split_images_single(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")]
        self.assertEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_images_at_start(self):
        node = TextNode("![alt](https://example.com/img.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_at_end(self):
        node = TextNode("Text followed by ![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text followed by ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_consecutive(self):
        node = TextNode("![first](url1)![second](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode("second", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_empty_alt(self):
        node = TextNode("![](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("", TextType.IMAGE, "https://example.com/img.png")]
        self.assertEqual(new_nodes, expected)

    def test_split_images_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_split_images_mixed_nodes(self):
        nodes = [
            TextNode("Text with ![image](url.png)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.png"),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("![image1](url1)", TextType.TEXT),
            TextNode("![image2](url2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode("image2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    # split_nodes_link tests
    def test_split_links_single(self):
        node = TextNode("[link text](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("link text", TextType.LINK, "https://example.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_links_at_start(self):
        node = TextNode("[link](url) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_at_end(self):
        node = TextNode("Text followed by [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text followed by ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_multiple(self):
        node = TextNode("Check [link1](url1) and [link2](url2) here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_consecutive(self):
        node = TextNode("[first](url1)[second](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("first", TextType.LINK, "url1"),
            TextNode("second", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_empty_text(self):
        node = TextNode("[](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("", TextType.LINK, "https://example.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_links_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("already bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_split_links_mixed_nodes(self):
        nodes = [
            TextNode("Text with [link](url)", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("already italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("[link1](url1)", TextType.TEXT),
            TextNode("[link2](url2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_links_with_special_chars_in_url(self):
        node = TextNode("[click here](https://example.com/path?query=1&other=2#anchor)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("click here", TextType.LINK, "https://example.com/path?query=1&other=2#anchor")]
        self.assertEqual(new_nodes, expected)

    def test_split_images_and_links_chained(self):
        nodes = [TextNode("Text with ![image](img.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        new_nodes = split_nodes_link(new_nodes)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(new_nodes, expected)

    # text_to_TextNode tests
    def test_text_to_textnode_plain_text(self):
        result = text_to_TextNode("Just plain text")
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnode_single_bold(self):
        result = text_to_TextNode("This is **bold** text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_single_italic(self):
        result = text_to_TextNode("This is _italic_ text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_single_code(self):
        result = text_to_TextNode("This is `code` text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_single_link(self):
        result = text_to_TextNode("This is [a link](https://example.com)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_single_image(self):
        result = text_to_TextNode("This is ![an image](https://example.com/img.png)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("an image", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_and_italic(self):
        result = text_to_TextNode("This is **bold** and _italic_ text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_and_code(self):
        result = text_to_TextNode("This is **bold** and `code` text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_italic_and_code(self):
        result = text_to_TextNode("This is _italic_ and `code` text")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_italic_code(self):
        result = text_to_TextNode("**bold** _italic_ `code`")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_all_formats_with_link(self):
        result = text_to_TextNode("This has **bold**, _italic_, `code`, and [a link](url.com)")
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_all_formats_with_image(self):
        result = text_to_TextNode("**bold** _italic_ `code` ![image](img.png)")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_all_markdown_features(self):
        result = text_to_TextNode(
            "This has **bold**, _italic_, `code`, ![image](img.png), and [a link](url.com)"
        )
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(", and ", TextType.TEXT),
            TextNode("a link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_bold(self):
        result = text_to_TextNode("**first bold** and **second bold**")
        expected = [
            TextNode("first bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_italic(self):
        result = text_to_TextNode("_first italic_ and _second italic_")
        expected = [
            TextNode("first italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_code(self):
        result = text_to_TextNode("`first code` and `second code`")
        expected = [
            TextNode("first code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_images(self):
        result = text_to_TextNode("![img1](url1) and ![img2](url2)")
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_multiple_links(self):
        result = text_to_TextNode("[link1](url1) and [link2](url2)")
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_nested_bold_italic(self):
        # Bold is processed first, so italic inside bold won't be parsed separately
        result = text_to_TextNode("**bold with _italic_ inside**")
        expected = [
            TextNode("bold with _italic_ inside", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_code_with_special_chars(self):
        # Code block must be properly matched - this test uses valid markdown
        result = text_to_TextNode("Use code `not bold` in text")
        expected = [
            TextNode("Use code ", TextType.TEXT),
            TextNode("not bold", TextType.CODE),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_link_with_complex_url(self):
        result = text_to_TextNode("[visit](https://example.com/path?query=1&other=2#anchor)")
        expected = [
            TextNode("visit", TextType.LINK, "https://example.com/path?query=1&other=2#anchor"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_image_then_link(self):
        result = text_to_TextNode("![image](img.png) [link](url.com)")
        expected = [
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_consecutive_formatting(self):
        result = text_to_TextNode("**bold**_italic_`code`")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_empty_string(self):
        result = text_to_TextNode("")
        # Empty strings are skipped during splitting
        expected = []
        self.assertEqual(result, expected)

    def test_text_to_textnode_whitespace_only(self):
        result = text_to_TextNode("   ")
        expected = [TextNode("   ", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_at_start(self):
        result = text_to_TextNode("**bold** text")
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold_at_end(self):
        result = text_to_TextNode("text **bold**")
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_link_with_bold_text(self):
        # Bold is processed first, so the markdown link inside won't be recognized
        result = text_to_TextNode("Check **this [link](url.com)**")
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this [link](url.com)", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is a single paragraph"
        blocks = markdown_to_blocks(md)
        expected = ["This is a single paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_two_blocks(self):
        md = "First paragraph\n\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        expected = ["First paragraph", "Second paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_multiple_blocks(self):
        md = "Block 1\n\nBlock 2\n\nBlock 3\n\nBlock 4"
        blocks = markdown_to_blocks(md)
        expected = ["Block 1", "Block 2", "Block 3", "Block 4"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "   First paragraph   \n\n   Second paragraph   "
        blocks = markdown_to_blocks(md)
        expected = ["First paragraph", "Second paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_multiple_empty_lines(self):
        md = "First\n\n\n\nSecond"
        blocks = markdown_to_blocks(md)
        # Triple newline creates three splits, but one of them is empty
        expected = ["First", "Second"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single_empty_lines(self):
        md = "First\nSecond\n\nThird"
        blocks = markdown_to_blocks(md)
        expected = ["First\nSecond", "Third"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_preserves_internal_newlines(self):
        md = "Line 1\nLine 2\nLine 3\n\nNewBlock"
        blocks = markdown_to_blocks(md)
        expected = ["Line 1\nLine 2\nLine 3", "NewBlock"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_heading(self):
        md = "# Heading\n\nParagraph under heading"
        blocks = markdown_to_blocks(md)
        expected = ["# Heading", "Paragraph under heading"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_multiple_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        blocks = markdown_to_blocks(md)
        expected = ["# Heading 1", "## Heading 2", "### Heading 3"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_list_block(self):
        md = "- Item 1\n- Item 2\n- Item 3\n\nParagraph"
        blocks = markdown_to_blocks(md)
        expected = ["- Item 1\n- Item 2\n- Item 3", "Paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_ordered_list(self):
        md = "1. Item 1\n2. Item 2\n3. Item 3\n\nParagraph"
        blocks = markdown_to_blocks(md)
        expected = ["1. Item 1\n2. Item 2\n3. Item 3", "Paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_code_block(self):
        md = "```\ncode here\nmore code\n```\n\nParagraph"
        blocks = markdown_to_blocks(md)
        expected = ["```\ncode here\nmore code\n```", "Paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_quote_block(self):
        md = "> Quote line 1\n> Quote line 2\n\nParagraph"
        blocks = markdown_to_blocks(md)
        expected = ["> Quote line 1\n> Quote line 2", "Paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_mixed_content(self):
        md = "# Main Title\n\nIntroduction paragraph\n\n- List item 1\n- List item 2\n\n> A quote\n> spans lines\n\nConclusion"
        blocks = markdown_to_blocks(md)
        expected = [
            "# Main Title",
            "Introduction paragraph",
            "- List item 1\n- List item 2",
            "> A quote\n> spans lines",
            "Conclusion",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_with_formatting(self):
        md = "**Bold** and _italic_ text\n\n`code` in paragraph\n\n[link](url)"
        blocks = markdown_to_blocks(md)
        expected = [
            "**Bold** and _italic_ text",
            "`code` in paragraph",
            "[link](url)",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_tabs_and_spaces(self):
        md = "\t\tFirst paragraph\t\t\n\n\t\tSecond paragraph\t\t"
        blocks = markdown_to_blocks(md)
        expected = ["First paragraph", "Second paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_newline_at_start(self):
        md = "\nParagraph 1\n\nParagraph 2"
        blocks = markdown_to_blocks(md)
        expected = ["Paragraph 1", "Paragraph 2"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_newline_at_end(self):
        md = "Paragraph 1\n\nParagraph 2\n"
        blocks = markdown_to_blocks(md)
        expected = ["Paragraph 1", "Paragraph 2"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_newlines_at_both_ends(self):
        md = "\nParagraph 1\n\nParagraph 2\n"
        blocks = markdown_to_blocks(md)
        expected = ["Paragraph 1", "Paragraph 2"]
        self.assertEqual(blocks, expected)

    # block_to_block_type tests
    def test_block_to_block_type_heading_h1(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h2(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h3(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h4(self):
        block = "#### Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h5(self):
        block = "##### Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_h6(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_no_space(self):
        block = "#NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_only_hashes(self):
        block = "####"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_simple(self):
        block = "```\ncode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_multiline(self):
        block = "```\nline 1\nline 2\nline 3\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_with_language(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_empty(self):
        block = "```\n\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_code_missing_end(self):
        block = "```\ncode here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_missing_start(self):
        block = "code here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_multiple_lines(self):
        block = "> Quote line 1\n> Quote line 2\n> Quote line 3"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_with_text(self):
        block = "> This is a longer quote\n> that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_quote_incomplete(self):
        block = "> Quote line 1\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote_no_space_after_arrow(self):
        block = ">No space"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list_dashes(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- Only item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_with_text(self):
        block = "- First item with text\n- Second item with text\n- Third item with text"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_incomplete(self):
        block = "- Item 1\n- Item 2\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_no_space_after_dash(self):
        block = "-NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list_asterisks(self):
        # This function uses dashes, not asterisks
        block = "* Item 1\n* Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_correct_sequence(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. Only item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_long_sequence(self):
        block = "1. One\n2. Two\n3. Three\n4. Four\n5. Five"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_wrong_start(self):
        block = "2. Item 1\n3. Item 2\n4. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_wrong_sequence(self):
        block = "1. Item 1\n3. Item 2\n2. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_incomplete(self):
        block = "1. Item 1\n2. Item 2\nNot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list_no_space_after_number(self):
        block = "1.NoSpace"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_plain_text(self):
        block = "This is a plain paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_formatting(self):
        block = "This is a paragraph with **bold** and _italic_"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiline(self):
        block = "Line 1\nLine 2\nLine 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_link(self):
        block = "This has a [link](url.com) in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_with_code_backticks(self):
        block = "This has `code` in it but is still a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_single_hash_middle(self):
        block = "This is text with # in the middle"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_quote_symbol_middle(self):
        block = "This is text with > in the middle"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_edge_case_just_dashes(self):
        block = "- "
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_edge_case_just_number_dot_space(self):
        block = "1. "
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_edge_case_just_arrow(self):
        block = ">"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_edge_case_mixed_quote_and_list(self):
        block = "> Quote\n- List"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()