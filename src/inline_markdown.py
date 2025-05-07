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


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text_so_far = node.text
        images = extract_markdown_images(text_so_far)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for (alt_text, url) in images:
            sections = text_so_far.split(f"![{alt_text}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section isn't closed")

            text_so_far = sections[1]

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

        if text_so_far != "":
            new_nodes.append(TextNode(text_so_far, TextType.PLAIN))

    return new_nodes


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text_so_far = node.text
        links = extract_markdown_links(text_so_far)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        for (alt_text, url) in links:
            sections = text_so_far.split(f"[{alt_text}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section isn't closed")

            text_so_far = sections[1]

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))

            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

        if text_so_far != "":
            new_nodes.append(TextNode(text_so_far, TextType.PLAIN))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.PLAIN)

    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
