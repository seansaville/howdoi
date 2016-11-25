#!/usr/bin/python3


"""
howdoi

Search a database of small pieces of information and output the results in the
terminal.
"""


import sys

from invertedindex import InvertedIndex


def main(argv):
    index = InvertedIndex()
    index.load_file("howdoi.json")

    query_tags = argv[1:]

    results = index.search(query_tags)
    if results:
        for result in results:
            # The term dictionary is keyed by integers, but the JSON serialiser
            # converts these to strings, so treat each document ID as a string.
            print(index.documents[str(result)])
    else:
        print("Couldn't find anything matching those tags!")


if __name__ == "__main__":
    main(sys.argv)
