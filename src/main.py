import os
import shutil

from copy_dir_content import copy_dir_content
from generate_content import generate_pages


DIR_PATH_PUBLIC = "./public"
DIR_PATH_STATIC = "./static"
DIR_PATH_CONTENT = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)

    print("Copying static files to public directory...")
    copy_dir_content(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

    generate_pages(DIR_PATH_CONTENT, DIR_PATH_PUBLIC, TEMPLATE_PATH)


if __name__ == "__main__":
    main()
