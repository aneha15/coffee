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
