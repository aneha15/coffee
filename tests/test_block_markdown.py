import unittest
from src.block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        text = "This is a single block of text."
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, ["This is a single block of text."])

    def test_multiple_blocks(self):
        text = """
This is the first block.

This is the second block.


This is the third block.
"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is the first block.",
                "This is the second block.",
                "This is the third block.",
            ],
        )

    def test_multiline_blocks(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "### This is a subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_fail(self):
        block = "#This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_fail(self):
        block = "``` python```"
        self.assertEqual(
            block_to_block_type(block), BlockType.PARAGRAPH
        )  # Not a valid code block, should be treated as paragraph

    def test_code(self):
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> spanning multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_fail(self):
        block = "> This is a quote\nThis is not part of the quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_fail(self):
        block = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_fail(self):
        block = "1. First item\n4. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph(self):
        block = "This is a regular paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_quotes(self):
        md = """
> This is a quote
> that spans multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote that spans multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3


"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )

    def test_heading_with_inline_formatting(self):
        md = """
## Hello **world**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Hello <b>world</b></h2></div>",
        )

    def test_all_heading_levels(self):
        md = """
# h1

## h2

### h3

#### h4

##### h5

###### h6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>h1</h1><h2>h2</h2><h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6></div>",
        )

    def test_unordered_list_with_asterisk(self):
        md = """
* Item 1
* Item 2
* Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_unordered_list_with_inline_formatting(self):
        md = """
- **bold** item
- _italic_ item
- `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li><li><code>code</code> item</li></ul></div>",
        )

    def test_ordered_list_with_inline_formatting(self):
        md = """
1. **bold** item
2. _italic_ item
3. `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>bold</b> item</li><li><i>italic</i> item</li><li><code>code</code> item</li></ol></div>",
        )

    def test_ordered_list_double_digits(self):
        md = """
1. item
2. item
3. item
4. item
5. item
6. item
7. item
8. item
9. item
10. item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li><li>item</li></ol></div>",
        )

    def test_quote_with_inline_formatting(self):
        md = """
> This is a **bold** quote with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote with <i>italic</i> text</blockquote></div>",
        )

    def test_codeblock_preserves_indentation(self):
        md = """
```
def foo():
    pass
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>def foo():\n    pass</code></pre></div>",
        )

    def test_codeblock_with_blank_lines(self):
        md = """
```
first line

second line
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>first line\n\nsecond line</code></pre></div>",
        )

    def test_unordered_list_star_marker(self):
        md = """
* Item 1
* Item 2
* Item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_unordered_list_with_inline_formatting(self):
        md = """
- **bold** item
- _italic_ item
- `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li><li><code>code</code> item</li></ul></div>",
        )

    def test_ordered_list_with_inline_formatting(self):
        md = """
1. **bold** item
2. _italic_ item
3. `code` item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li><b>bold</b> item</li><li><i>italic</i> item</li><li><code>code</code> item</li></ol></div>",
        )

    def test_ordered_list_double_digit(self):
        md = "\n".join(f"{i}. item {i}" for i in range(1, 11))
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 11))
        self.assertEqual(html, f"<div><ol>{expected_items}</ol></div>")

    def test_quote_with_inline_formatting(self):
        md = """
> This is a **bold** quote
> with _italic_ text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote with <i>italic</i> text</blockquote></div>",
        )

    def test_paragraph_with_link(self):
        md = """
This is a [link](https://example.com) in a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a <a href="https://example.com">link</a> in a paragraph</p></div>',
        )

    def test_paragraph_with_image(self):
        md = """
This is an ![image](https://example.com/img.png) in a paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is an <img src="https://example.com/img.png" alt="image"> in a paragraph</p></div>',
        )

    def test_multiple_blocks_mixed(self):
        md = """
# Title

This is a paragraph with **bold** text.

- item one
- item two

> a quote

```
some code
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>item one</li><li>item two</li></ul><blockquote>a quote</blockquote><pre><code>some code</code></pre></div>",
        )

    def test_multiple_blank_lines_between_blocks(self):
        md = """
# Heading



A paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>A paragraph.</p></div>",
        )

    def test_invalid_input_type_raises(self):
        with self.assertRaises(TypeError):
            markdown_to_html_node(123)

    def test_empty_string(self):
        node = markdown_to_html_node("")
        html = node.to_html()
        self.assertEqual(html, "<div></div>")


if __name__ == "__main__":
    unittest.main()
