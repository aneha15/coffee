import unittest
from src.inline_markdown import split_nodes_delimiter
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
        print(result)
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
                TextNode(" here.", TextType.TEXT)
            ],
        )
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("here is some **bold** text. ", TextType.TEXT),
            TextNode("more **bold** text", TextType.TEXT)
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
                TextNode(" text", TextType.TEXT)
            ]
        )
    
    def test_delimiters_at_end(self):
        nodes = [TextNode("._..._", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode(".", TextType.TEXT), TextNode("...", TextType.ITALIC)])

    
    def test_delimiters_at_start(self):
        nodes = [TextNode("_..._.", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(result, [TextNode("...", TextType.ITALIC), TextNode(".", TextType.TEXT)])
        
