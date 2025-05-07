import os
import shutil
import sys

from copy_dir_content import copy_dir_content
from generate_content import generate_pages


DIR_PATH_DOCS = "./docs"
DIR_PATH_STATIC = "./static"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting public directory...")
    if os.path.exists(DIR_PATH_DOCS):
        shutil.rmtree(DIR_PATH_DOCS)

    print("Copying static files to public directory...")
    copy_dir_content(DIR_PATH_STATIC, DIR_PATH_DOCS)

    generate_pages(
        src=DIR_PATH_CONTENT,
        dst=DIR_PATH_DOCS,
        template_path=TEMPLATE_PATH,
        basepath=basepath
    )


if __name__ == "__main__":
    main()
