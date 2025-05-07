def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    mapped = map(lambda str: str.strip(), blocks)
    filtered = filter(lambda str: str != "", mapped)

    return list(filtered)
