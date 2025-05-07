import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("string with some `code` in it", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual(nodes, [
            TextNode("string with some ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.PLAIN)
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image alt text](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image alt text", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a [link text](https://google.com) and an ![image](https://placehold.co/600x400)")

        self.assertListEqual(matches, [("link text", "https://google.com")])


if __name__ == "__main__":
    unittest.main()
