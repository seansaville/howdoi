#!/usr/bin/python3


"""
howdoi

Searchable command-line database designed for small pieces of information (e.g.
terminal commands)
"""


import argparse
import os.path
from sys import stdin

from invertedindex import InvertedIndex


def add(index, terms):
    """
    Add a document, consisting of the concatenation of the query tags, to the
    provided inverted index.
    """

    document = " ".join(terms)

    print("I'm going to add \"{}\" to the database.".format(document))
    print("Type some additional tags for this item (separated by spaces). "
          "Hit Enter to skip, or type ! to cancel adding this item:")

    # Strip newline characters from the line before we split it into tags
    extra_tags = stdin.readline().replace("\r", "").replace("\n", "").split(" ")

    if "!" not in extra_tags:
        if "" not in extra_tags:
            index.add_document(document, extra_tags)
        else:
            index.add_document(document, [])

        index.save_to_file("howdoi.json")
        print("Command added and database updated.")
    else:
        print("Nothing was changed.")


def search(index, tags):
    """
    Search the index for the provided tags and print the matching documents.
    """

    results = index.search(tags)
    if results:
        for result in results:
            # The term dictionary is keyed by integers, but the JSON serialiser
            # converts these to strings, so treat each document ID as a string.
            print(index.documents[str(result)])
    else:
        print("Couldn't find anything matching those tags!")


def main():
    """
    Main function. Parses command-line arguments and performs the appropriate
    action.
    """

    parser = argparse.ArgumentParser(description="Searchable command-line "
                                     "database designed for small pieces of "
                                     "information (e.g. terminal commands)")
    parser.add_argument("-a", "--add", action="store_true",
                        help="insert the query text into the database instead")
    parser.add_argument("TAGS", nargs="+", help="tags forming the query text")
    args = parser.parse_args()

    index = InvertedIndex()

    # If the database isn't where we expect it, then save a new one to disk.
    if not os.path.isfile("howdoi.json"):
        print("Couldn't find the database, so a new one was created.")
        index.save_to_file("howdoi.json")

    try:
        index.load_from_file("howdoi.json")
        if args.add:
            add(index, args.TAGS)
        else:
            search(index, args.TAGS)
    except IOError:
        print("Hit a file-related error somewhere :(")


if __name__ == "__main__":
    main()
