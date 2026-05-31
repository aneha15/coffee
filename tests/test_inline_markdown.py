import unittest
from src.inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.text_node import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(result, nodes)

    def test_unclosed_delimiter(self):
        nodes = [TextNode("Hello **world", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_non_text_node(self):
        nodes = [TextNode("Hello World", TextType.ITALIC)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(nodes, result)

    def test_single_section(self):
        nodes = [TextNode("Hello `there` world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("there", TextType.CODE),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def test_multiple_sections(self):
        nodes = [TextNode("Hello `there` world. More `code` here.", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("there", TextType.CODE),
                TextNode(" world. More ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here.", TextType.TEXT),
            ],
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("here is some **bold** text. ", TextType.TEXT),
            TextNode("more **bold** text", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("here is some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text. ", TextType.TEXT),
                TextNode("more ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiters_at_end(self):
        nodes = [TextNode("._..._", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            result, [TextNode(".", TextType.TEXT), TextNode("...", TextType.ITALIC)]
        )

    def test_delimiters_at_start(self):
        nodes = [TextNode("_..._.", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            result, [TextNode("...", TextType.ITALIC), TextNode(".", TextType.TEXT)]
        )


class TestExtractMarkdownImages(unittest.TestCase):
    def test_no_images(self):
        text = "text only"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_single_image(self):
        text = "Here is an image: ![alt text](http://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "http://example.com/image.jpg")])

    def test_multiple_images(self):
        text = "First image: ![first](http://example.com/first.jpg) and second image: ![second](http://example.com/second.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result,
            [
                ("first", "http://example.com/first.jpg"),
                ("second", "http://example.com/second.jpg"),
            ],
        )

    def test_wrong_image_syntax(self):
        text = "This is not an image: ![alt text(http://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_link_syntax(self):
        text = "link: [Google](http://google.com)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_no_links(self):
        text = "no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_single_link(self):
        text = "Here is a link: [Google](http://google.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Google", "http://google.com")])

    def test_multiple_links(self):
        text = "First link: [Google](http://google.com) and second link: [GitHub](http://github.com)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result, [("Google", "http://google.com"), ("GitHub", "http://github.com")]
        )

    def test_wrong_link_syntax(self):
        text = "This is not a link: [Google(http://google.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_image_syntax(self):
        text = "image: ![first](http://example.com/first.jpg)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])


class TestSplitNodesImage(unittest.TestCase):
    def test_no_images(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, nodes)

    def test_single_image(self):
        nodes = [
            TextNode("image: ![alt text](http://example.com/image.jpg)", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("image: ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "http://example.com/image.jpg"),
            ],
        )

    def test_multiple_images(self):
        nodes = [
            TextNode(
                "First image: ![first](http://example.com/first.jpg) and second image: ![second](http://example.com/second.jpg)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("First image: ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "http://example.com/first.jpg"),
                TextNode(" and second image: ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "http://example.com/second.jpg"),
            ],
        )

    def test_image_in_between(self):
        nodes = [
            TextNode(
                "Here is an image: ![alt text](http://example.com/image.jpg) in the middle of text.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "http://example.com/image.jpg"),
                TextNode(" in the middle of text.", TextType.TEXT),
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, nodes)

    def test_single_link(self):
        nodes = [TextNode("link: [Google](http://google.com)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("link: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "http://google.com"),
            ],
        )

    def test_multiple_links(self):
        nodes = [
            TextNode(
                "First link: [Google](http://google.com) and second link: [GitHub](http://github.com)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("First link: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "http://google.com"),
                TextNode(" and second link: ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "http://github.com"),
            ],
        )

    def test_link_in_between(self):
        nodes = [
            TextNode(
                "Here is a link: [Google](http://google.com) in the middle of text.",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Here is a link: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "http://google.com"),
                TextNode(" in the middle of text.", TextType.TEXT),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "Hello world"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Hello world", TextType.TEXT)])

    def test_bold_and_italic(self):
        text = "This is **bold** and _italic_ text."
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_code_and_link(self):
        text = "Here is some `code` and a [link](http://example.com)."
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Here is some ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_image_and_bold(self):
        text = (
            "Here is an image: ![alt](http://example.com/image.jpg) and **bold** text."
        )
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("Here is an image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text.", TextType.TEXT),
            ],
        )

    def test_all_markdown(self):
        text = "This is **bold**, _italic_, `code`, a [link](http://example.com), and an image: ![alt](http://example.com/image.jpg)."
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://example.com"),
                TextNode(", and an image: ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg"),
                TextNode(".", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
