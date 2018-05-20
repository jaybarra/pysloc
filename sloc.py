import os
import argparse
import operator


def get_source_files(entry="./", extensions=None, ignore=None):
    """
    Returns an array of source code files
    :param entry:
    :param extensions:
    :param ignore:
    :return:
    """

    if extensions is None:
        extensions = [".js", ".jsx", "css", "html", ".jsp", ".py", ".h", ".hh", ".c", ".cpp", ".cxx", ".java"]

    if ignore is None:
        ignore = ["node_modules", "vendor", ".git", ".cvs", ".svn", ".hg", "dist", "bin", "target", "out", ".idea"]

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


def lines_in_file(f):
    """
    Returns line count of the file as a tuple
    :param f:
    :return:
    """
    f.replace("\\", "/")

    total_line_count = 0
    blank_line_count = 0
    comment_line_count = 0
    source_line_count = 0

    in_comment_block = False

    file_type = f.split(".")[-1]

    with open(f) as src:
        try:
            for total_line_count, line in enumerate(src):

                in_comment_block = check_for_comment_block(line, file_type)

                if not line.strip():
                    blank_line_count += 1
                elif in_comment_block or is_comment(line, file_type):
                    comment_line_count += 1
                else:
                    source_line_count += 1

            total_line_count += 1
        except IOError:
            pass

    return total_line_count, source_line_count, comment_line_count, blank_line_count


def check_for_comment_block(line, file_type):
    """

    :param line:
    :param file_type:
    :return:
    """
    line = line.strip()

    if file_type == "py":
        return line.startswith('"""') and ('"""' not in line and len(line) > 3)

    if file_type in ["java", "js", "jsx", "c", "cpp", "cxx", "h"]:
        return line.startswith("/*") and "*/" not in line

    if file_type in ["jsp"]:
        return line.startswith("<%--") and not line.endswith("%-->")


def is_comment(line, file_type=None):
    """

    :param line:
    :param file_type:
    :param in_comment_block:
    :return:
    """
    line = line.strip()

    if file_type in ["java", "js", "jsx", "c", "cpp", "cxx", "h", "hh"]:
        return line.startswith("//") or line.startswith("/*")

    if file_type in ["py", "sh"]:
        return line.startswith("#") or line.startswith('"""')

    if file_type in ["jsp"]:
        return line.startswith("<%--")

    if file_type in ["html", "xml"]:
        return line.startswith("<!--")

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('target', nargs='?', default=os.getcwd())

    args = parser.parse_args()
    source_files = get_source_files(args.target)

    file_count = {}
    total_sloc = 0, 0, 0, 0

    for f in source_files:
        file_type = f.split(".")[-1]

        file_sloc = lines_in_file(f)
        total_sloc = tuple(map(sum, zip(file_sloc, total_sloc)))

        if file_type not in file_count:
            file_count[file_type] = 1
        else:
            file_count[file_type] = file_count[file_type] + 1

        print("{sloc} : {file}".format(sloc=str(file_sloc[1]).rjust(4), file=f))

    print("=" * 80)
    print("""
    SLOC Evaluation:
    Total Lines:   %6d
    Source Lines:  %6d
    Comment Lines: %6d
    Blank Lines:   %6d
    """ % total_sloc)

    print(file_count)
