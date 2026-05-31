import re
from src.text_node import TextNode, TextType


def split_nodes_delimiter(
    nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for n in nodes:
        # only split nodes in plain text
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue

        parts = n.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Invalid markdown syntax: Delimiter '{delimiter}' was never closed"
            )

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                # plain text
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # formatted text
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def extract_markdown_images(text):
    # regex that matches markdown image syntax ![alt text](url)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    images = []

    for alt_text, url in matches:
        images.append((alt_text, url))

    return images


def extract_markdown_links(text):
    # regex that matches markdown link syntax ![anchor text](url)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    links = []

    for anchor_text, url in matches:
        links.append((anchor_text, url))

    return links


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for n in nodes:
        imgs = extract_markdown_images(n.text)

        if not imgs:
            new_nodes.append(n)
            continue

        sections = n.text
        for text, url in imgs:
            sections = sections.split(f"![{text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.IMAGE, url))
                sections = sections[1]

    return new_nodes


def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for n in nodes:
        links = extract_markdown_links(n.text)

        if not links:
            new_nodes.append(n)
            continue

        sections = n.text
        for text, url in links:
            sections = sections.split(f"[{text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                sections = sections[1]

    return new_nodes
