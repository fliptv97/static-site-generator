import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def generate_pages(src, dst, template_path, basepath):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)

        if os.path.isfile(src_path):
            generate_page(
                os.path.join(src_path),
                os.path.join(Path(dst_path).with_suffix(".html")),
                template_path,
                basepath
            )
        else:
            generate_pages(src_path, dst_path, template_path, basepath)


def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("markdown must have at least one level 1 header")


def generate_page(src, dst, template_path, basepath):
    print(f"Generating page from {src} to {dst} using {template_path}")

    with open(src, encoding="utf-8") as markdown_file:
        with open(template_path, encoding="utf-8") as template_file:
            markdown = markdown_file.read()
            title = extract_title(markdown)
            node = markdown_to_html_node(markdown)
            content = node.to_html()
            template = template_file.read()
            page = template.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", content)
            page = page.replace("href=\"/", f"href=\"{basepath}")
            page = page.replace("src=\"/", f"src=\"{basepath}")

            os.makedirs(os.path.dirname(dst), exist_ok=True)

            with open(dst, "w", encoding="utf-8") as html_file:
                html_file.write(page)
