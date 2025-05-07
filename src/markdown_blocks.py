from enum import Enum
import re


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
