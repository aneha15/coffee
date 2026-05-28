from textnode import TextType, TextNode


def main():
    n = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
    print(n.text_type)


main()
