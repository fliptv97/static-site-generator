import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "Click Here!", None, {
            "target": "_blank",
            "href": "http://localhost:8888/not-found"
        })

        self.assertEqual(
            node.props_to_html(),
            " target=\"_blank\" href=\"http://localhost:8888/not-found\""
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Lorem Ipsum")

        self.assertEqual(node.to_html(), "<p>Lorem Ipsum</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "click here", {
            "target": "_blank",
            "href": "http://localhost:8888/not-found"
        })

        self.assertEqual(
            node.to_html(),
            "<a target=\"_blank\" href=\"http://localhost:8888/not-found\">click here</a>"
        )

    def test_to_html_without_tag(self):
        node = LeafNode(None, "hello world")

        self.assertEqual(node.to_html(), "hello world")

    def test_to_html_without_value(self):
        node = LeafNode("a", None)

        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode("b", "child")])

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_without_children(self):
        node = ParentNode("div", None)

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_props(self):
        node = ParentNode("div", [LeafNode("span", "lorem ipsum")], {
            "class": "wrapper"
        })

        self.assertEqual(node.to_html(), "<div class=\"wrapper\"><span>lorem ipsum</span></div>")


if __name__ == "__main__":
    unittest.main()
