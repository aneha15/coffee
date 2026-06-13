from enum import Enum
import re
from src.html_node import HTMLNode, LeafNode, ParentNode
from src.text_node import text_node_to_html_node
from src.inline_markdown import text_to_textnodes


def markdown_to_blocks(text: str) -> list[str]:
    blocks = []
    current = []
    in_code_block = False

    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            current.append(line)
        elif not in_code_block and line.strip() == "":
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            if in_code_block:
                current.append(line)
            else:
                current.append(line.strip())

    if current:
        blocks.append("\n".join(current))

    return [b for b in blocks if b.strip()]


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE

    lines = block.splitlines()

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(re.match(r"^[-*] ", line) for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(rf"^{i+1}\. ", line) for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(md: str) -> HTMLNode:
    if not isinstance(md, str):
        raise TypeError(f"Expected str, got {type(md).__name__}")

    blocks = markdown_to_blocks(md)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)

        case BlockType.HEADING:
            return heading_to_html_node(block)

        case BlockType.QUOTE:
            return quote_to_html_node(block)

        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)

        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)

        case BlockType.CODE:
            return code_to_html_node(block)
        case _:
            raise ValueError(f"Unhandled block type: {block_type}")


def paragraph_to_html_node(block: str) -> HTMLNode:
    text = " ".join(block.splitlines())
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> HTMLNode:
    m = re.match(r"^(#{1,6}) ", block)
    if not m:
        raise ValueError(f"Invalid heading block: {block!r}")
    level = len(m.group(1))
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def quote_to_html_node(block: str) -> HTMLNode:
    text = " ".join(line.lstrip(">").strip() for line in block.splitlines())
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = [re.sub(r"^[-*] ", "", line) for line in block.splitlines()]
    return ParentNode("ul", [ParentNode("li", text_to_children(i)) for i in items])


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = [re.sub(r"^\d+\.\s+", "", line) for line in block.splitlines()]
    return ParentNode("ol", [ParentNode("li", text_to_children(i)) for i in items])


def code_to_html_node(block: str) -> HTMLNode:
    code = block.removeprefix("```\n").removesuffix("\n```")
    return ParentNode("pre", [LeafNode("code", code)])


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]
