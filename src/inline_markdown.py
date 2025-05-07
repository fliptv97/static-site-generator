import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        splits = node.text.split(delimiter)

        if len(splits) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for idx, split in enumerate(splits):
            if split == "":
                continue

            if idx % 2 == 0:
                new_nodes.append(TextNode(split, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(split, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
