#!/usr/bin/python3


"""
howdoi

Search a database of small pieces of information and output the results in the
terminal.
"""


import argparse

from invertedindex import InvertedIndex


def main():
    parser = argparse.ArgumentParser(description="Searchable command-line "
                                     "database designed for small pieces of "
                                     "information (e.g. terminal commands)")
    parser.add_argument("-a", "--add", action="store_true",
                        help="insert the query text into the database instead")
    parser.add_argument("TAGS", nargs="+", help="tags forming the query text")
    args = parser.parse_args()

    index = InvertedIndex()
    index.load_file("howdoi.json")

    query_tags = args.TAGS

    results = index.search(query_tags)
    if results:
        for result in results:
            # The term dictionary is keyed by integers, but the JSON serialiser
            # converts these to strings, so treat each document ID as a string.
            print(index.documents[str(result)])
    else:
        print("Couldn't find anything matching those tags!")


if __name__ == "__main__":
    main()
