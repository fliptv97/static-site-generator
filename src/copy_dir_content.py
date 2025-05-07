import os
import shutil

def copy_dir_content(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)

        if os.path.isfile(src_path):
            print(f"copying {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_dir_content(src_path, dst_path)
