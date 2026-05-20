import unittest

from markdown_to_html import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_heading_hash_and_whitespace(self):
        self.assertEqual(extract_title("  #  My Title  "), "My Title")

    def test_first_h1_in_document(self):
        md = """Some intro line

# Page Title

## Not the title
"""
        self.assertEqual(extract_title(md), "Page Title")

    def test_skips_h2_and_finds_h1(self):
        md = """## Sub first
# Real Title
"""
        self.assertEqual(extract_title(md), "Real Title")

    def test_no_h1_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just plain text\n\nNo heading here.")

    def test_only_h2_raises(self):
        with self.assertRaises(ValueError):
            extract_title("## Only h2\n\nParagraph.")

    def test_h1_without_space_after_hash(self):
        self.assertEqual(extract_title("#Tight"), "Tight")


if __name__ == "__main__":
    unittest.main()
