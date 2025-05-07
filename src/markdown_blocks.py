from enum import Enum
import re

from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    mapped = map(lambda str: str.strip(), blocks)
    filtered = filter(lambda str: str != "", mapped)

    return list(filtered)


def block_to_block_type(block):
    if re.match(r"#{1,6}\s", block) is not None:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_ordered_list(lines):
    counter = 1

    for line in lines:
        if not line.startswith(f"{counter}. "):
            return False
        counter += 1

    return True

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match (block_type):
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case _:
                raise ValueError(f"invalid or unsupported block type: {block_type}")

    return ParentNode("div", children)


def paragraph_to_html_node(block):
    paragraph = block.replace("\n", " ")
    children = text_to_children(paragraph)

    return ParentNode("p", children)


def heading_to_html_node(block):
    parts = block.split(" ", 1)

    if parts[1] == "":
        raise ValueError("heading must not be empty")

    level = len(parts[0])
    children = text_to_children(parts[1])

    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    text_node = TextNode(block[4:-3], TextType.PLAIN)
    html_node = text_node_to_html_node(text_node)
    code = ParentNode("code", [html_node])
    pre = ParentNode("pre", [code])

    return pre


def quote_to_html_node(block):
    children = text_to_children(block.replace("> ").replace("\n", " "))
    blockquote = ParentNode("blockquote", children)

    return blockquote


def unordered_list_to_html_node(block):
    lines = block.splitlines()
    list_items = map(lambda line: ParentNode("li", text_to_children(line[2:])), lines)
    ul = ParentNode("ul", list_items)

    return ul


def ordered_list_to_html_node(block):
    lines = block.splitlines()
    list_items = map(lambda line: ParentNode("li", text_to_children(line[2:])), lines)
    ul = ParentNode("ol", list_items)

    return ul


def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    return list(map(text_node_to_html_node, text_nodes))
