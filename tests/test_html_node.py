import unittest
from src.html_node import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_node_to_html(self):
        node = HTMLNode("div", "...")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_empty(self):
        node1 = HTMLNode("div", "...", props=None)
        node2 = HTMLNode("div", "...", props={})

        self.assertEqual(node1.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")

    def test_props_to_html_formatted(self):
        node = HTMLNode(
            "a",
            "link",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode("h1", "heading")
        expected = f"tag: h1, value: heading, children: None, props: None"
        self.assertEqual(repr(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "...")
        self.assertEqual(node.to_html(), node.value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "this is a para")
        self.assertEqual(node.to_html(), "<p>this is a para</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me</a>'
        )

    def test_repr(self):
        node = LeafNode("p", "this is a para")
        self.assertEqual(repr(node), "tag: p, value: this is a para, props: None")


class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "...")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_props(self):
        node = ParentNode("div", [LeafNode("p", "para1")], {"class": "container"})
        self.assertEqual(node.to_html(), '<div class="container"><p>para1</p></div>')

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


if __name__ == "__main__":
    unittest.main()
