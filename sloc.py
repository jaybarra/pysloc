import os
import re
import argparse
import glob

def get_source_files(entry = "./", extensions = [".js", ".jsx", ".py", ".h", ".hh", ".c", ".cpp", ".cxx", ".java"], ignore = ["node_modules", "vendor", ".git", ".cvs", ".svn", ".hg", "dist", "bin"]):
    """Returns an array of source code files"""
    source_files = []
    for root, dirs, files in os.walk(entry, topdown=False):
        # Exclude ignored directories
        dirs[:] = [d for d in dirs if d not in ignore]

        # Exclude minified files
        files[:] = [f for f in files if ".min." not in f]

        # Filter out filetypes
        for name in files:
            for ext in extensions:
                if name.endswith(ext):
                    source_files.append(os.path.join(root, name))
    return source_files

def file_len(f):
    """Returns the file length of the file"""
    f.replace("\\", "/")
    with open(f) as src:
        try:
            for i, line in enumerate(src):
                pass
            return i + 1
        except:
            return -1

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--directory", default="./")
    args = parser.parse_args()

    source_files = get_source_files(args.directory);

    total_sloc = 0
    for f in source_files:
        file_sloc = file_len(f)
        total_sloc += file_sloc
        print("{sloc} : {file}".format(sloc=str(file_sloc).rjust(4), file=f))

    print("=" * 80)
    print(str(total_sloc) + " Total SLOC")

if __name__ == "__main__": main()
