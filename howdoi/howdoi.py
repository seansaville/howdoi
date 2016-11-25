#!/usr/bin/python3


"""
howdoi

Search a database of small pieces of information and output the results in the
terminal.
"""


import argparse
from sys import stdin

from invertedindex import InvertedIndex


def add(index, tags):
    """
    Add a document, consisting of the concatenation of the tags, to the provided
    index.
    """

    document = " ".join(tags)

    print("I'm going to add \"{}\" to the database.".format(document))
    print("Type some additional tags for this item (separated by spaces). "
          "Hit Enter to skip, or use ^C to cancel adding this item:")

    # Strip newline characters from the line before we split it into tags
    extra_tags = stdin.readline().replace("\r", "").replace("\n", "").split(" ")

    index.add_document(document, extra_tags)
    index.save_to_file("howdoi.json")


def search(index, tags):
    """
    Search the index for the provided tags and print the matching documents.
    """

    results = index.search(tags)
    if results:
        for result in results:
            # The term dictionary is keyed by integers, but the JSON
            # serialiser converts these to strings, so treat each document
            # ID as a string.
            print(index.documents[str(result)])
    else:
        print("Couldn't find anything matching those tags!")



def main():
    """
    Main function for howdoi
    """

    parser = argparse.ArgumentParser(description="Searchable command-line "
                                     "database designed for small pieces of "
                                     "information (e.g. terminal commands)")
    parser.add_argument("-a", "--add", action="store_true",
                        help="insert the query text into the database instead")
    parser.add_argument("TAGS", nargs="+", help="tags forming the query text")
    args = parser.parse_args()

    index = InvertedIndex()
    index.load_from_file("howdoi.json")

    if args.add:
        add(index, args.TAGS)
    else:
        search(index, args.TAGS)


if __name__ == "__main__":
    main()
