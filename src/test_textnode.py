import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

        url = "http://localhost:8888/placeholder.png"
        image_node = TextNode("This is an image node", TextType.IMAGE, url)
        image_node2 = TextNode("This is an image node", TextType.IMAGE, url)

        self.assertEqual(image_node, image_node2)

        link_node = TextNode("This is a link node", TextType.LINK, url)

        self.assertNotEqual(image_node, link_node)

    def test_default_url(self):
        node = TextNode("Image node example", TextType.LINK)

        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("Placeholder text", TextType.PLAIN)

        self.assertEqual(repr(node), "TextNode(Placeholder text, plain, None)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()
