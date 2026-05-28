from traceback import TracebackException
import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_text_type(self):
        node1 = TextNode("this is a text node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("this is a text node", TextType.LINK)
        node2 = TextNode("this is a text node", TextType.LINK, "https://www.e.com")
        self.assertNotEqual(node1, node2)

    def test_text(self):
        text_node = TextNode("....", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "....")

    def test_bold_(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_code(self):
        text_node = TextNode("print()", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print()")

    def test_link(self):
        text_node = TextNode("Click", TextType.LINK, "https://www.e.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click")
        self.assertEqual(html_node.props, {"href": "https://www.e.com"})

    def test_image(self):
        text_node = TextNode("image desc", TextType.IMAGE, "https://e.com/d.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://e.com/d.jpg", "alt": "image desc"}
        )

    def test_invalid_type(self):
        class xyz:
            pass

        text_node = TextNode("inv", xyz)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()
