import argparse
import sys

from multitool.runner import (binprint, contains, dirinfo, empty_files,
                              find_duplicates, ordprint, synonyms, utf)


def execute(args=None):
    """
    Operate the main function for program.
    """
    if not args:
        if not sys.argv[1:]:
            args = ["-h"]
        else:
            args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        "multitool", description="Multitool CLI", prefix_chars="-"
    )

    parsers = parser.add_subparsers()

    binparser = parsers.add_parser("bin", help="Convert integers to binary")

    binparser.add_argument("value", help="Integer to convert", action="store")

    binparser.set_defaults(func=binprint)

    ordparser = parsers.add_parser(
        "ord", help="Convert characters into ordinal"
    )

    ordparser.add_argument(
        "chars", help="Characters to convert", action="store"
    )

    ordparser.set_defaults(func=ordprint)

    synparse = parsers.add_parser("syn", help="get synonyms for commong words")

    emptyparser = parsers.add_parser("empty", help="Empty file remover")

    emptyparser.add_argument(
        "path",
        help="base directory and starting point.",
        nargs="*",
        action="store",
    )

    emptyparser.add_argument(
        "-d",
        "--dir",
        help="remove empty directories instead of empty files.",
        dest="folders",
        action="store_true",
    )

    emptyparser.add_argument(
        "--exclude-names",
        help="one or more file/directory names that will be ignored while "
        "searching for items to remove.",
        nargs="+",
        dest="ex_names",
        default=[],
    )

    emptyparser.add_argument(
        "--exclude-ext",
        help="one or more file extensions to be ignored during "
        "file/directory analysis.",
        nargs="+",
        dest="ex_ext",
        default=[],
    )

    emptyparser.add_argument(
        "-l",
        "--list",
        help="list the files to be deleted",
        action="store_true",
        dest="list",
    )

    emptyparser.add_argument(
        "-c",
        "--confirm",
        help="require confirmation before deleting",
        action="store_true",
        dest="confirm",
    )

    emptyparser.set_defaults(func=empty_files)

    synparse.add_argument(
        "word",
        help="Show Synonyms for the word",
        action="store",
        metavar="<word>",
    )

    synparse.add_argument(
        "-p",
        "--precision",
        help="how many similar words to include with the original.",
        dest="precision",
        action="store",
        metavar="<n>",
        default="1",
    )

    synparse.set_defaults(func=synonyms)

    containsparser = parsers.add_parser(
        "contains", help="Show words that contain <text>."
    )

    containsparser.add_argument(
        "--start",
        help="Show words that start with <text>",
        dest="start",
        metavar="<text>",
        action="store",
    )

    containsparser.add_argument(
        "--end",
        help="Show words that end with <text>",
        dest="end",
        metavar="<text>",
        action="store",
    )

    containsparser.add_argument(
        "-l",
        "--length",
        help="number <n> of characters in word",
        dest="length",
        metavar="<n>",
        action="store",
    )

    containsparser.set_defaults(func=contains)

    utfparser = parsers.add_parser(
        "utf", help="print unicode characters to terminal"
    )

    utfparser.add_argument(
        "number",
        help="one or more space seperated utf-8 codepoint(s)",
        nargs="*",
        action="store",
        default=None,
    )

    utfparser.add_argument(
        "-r",
        "--range",
        nargs=2,
        metavar="<number>",
        dest="range",
        action="store",
    )

    utfparser.add_argument(
        "-l",
        "--list",
        help="show each code, number combo on seperate lines.",
        action="store_true",
        dest="list",
    )

    utfparser.add_argument(
        "--line",
        help="like list except prints as many combos on a line as possible",
        action="store_true",
        dest="line",
    )

    utfparser.set_defaults(func=utf)

    dirparser = parsers.add_parser("dir", help="directory information")

    dirparser.add_argument("path", help="directory path")

    dirparser.add_argument(
        "-s", help="total size of contents", dest="size", action="store_true"
    )

    dirparser.add_argument(
        "-c",
        dest="count",
        help="total count of all files recusively",
        action="store_true",
    )

    dirparser.set_defaults(func=dirinfo)

    dupparser = parsers.add_parser(
        "dup", help="Find duplicate files within the same directory"
    )

    dupparser.add_argument(
        "-a",
        "--auto",
        action="store_true",
        dest="auto",
        help="don't prompt before deleting",
    )

    dupparser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        dest="recursive",
        help="search through folder recursively",
    )

    dupparser.add_argument(
        "dir", action="store", metavar="<dir>", help="directory to search."
    )

    dupparser.set_defaults(func=find_duplicates)

    namespace = parser.parse_args(args)

    print(namespace)

    return namespace.func(namespace)
