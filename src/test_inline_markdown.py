import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links
)


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


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://google.com) and another [link](https://gmail.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://gmail.com"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
