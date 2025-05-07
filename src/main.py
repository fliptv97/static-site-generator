import os
import shutil

from copy_dir_content import copy_dir_content


DIR_PATH_PUBLIC = "./public"
DIR_PATH_STATIC = "./static"


def main():
    print("Deleting public directory...")
    if os.path.exists(DIR_PATH_PUBLIC):
        shutil.rmtree(DIR_PATH_PUBLIC)

    print("Copying static files to public directory...")
    copy_dir_content(DIR_PATH_STATIC, DIR_PATH_PUBLIC)


if __name__ == "__main__":
    main()
