#!/usr/bin/env python3


"""
howdoi

Searchable command-line database designed for small pieces of information (e.g.
terminal commands)
"""


import argparse
import os.path
from sys import stdin

from invertedindex import InvertedIndex


DB_FILE_NAME = "db.howdoi"


def add(index, terms):
    """
    Add a document, consisting of the concatenation of the query tags, to the
    provided inverted index.
    """

    document = " ".join(terms)

    print("I'm going to add \"{}\" to the database.".format(document))
    print("By default, each significant word in the string is a search tag.")
    print("If you want to provide your own tags INSTEAD, provide them now.")
    print("Hit Enter to skip, or type ! to cancel adding this item:")

    # Strip newline characters from the line before we split it into tags
    custom_tags = stdin.readline().replace("\r", "").replace("\n", "").split(" ")

    if "!" not in custom_tags:
        if "" not in custom_tags:
            index.add_document(document, custom_tags)
        else:
            index.add_document(document, [])

        index.save_to_file(DB_FILE_NAME)
        print("Command added and database updated.")
    else:
        print("Nothing was changed.")


def delete(index, doc_id):
    """
    Delete the document with the provided ID from the index.
    """

    doc_id = str(doc_id[0])
    if index.delete_document(doc_id):
        index.save_to_file(DB_FILE_NAME)
        print("Deleted item {}".format(doc_id))
    else:
        print("Can't delete item {} - it doesn't exist!".format(doc_id))


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


def show(index):
    """
    Print the documents stored in the index along with their document IDs.
    """

    if not index.documents:
        print("Database is empty!")
    else:
        for doc_id in index.documents:
            print("{}: {}".format(doc_id, index.documents[doc_id]))


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
    parser.add_argument("-d", "--delete", nargs=1, metavar="DOCID", type=int,
                        help="delete item with document ID DOCID")
    parser.add_argument("-s", "--show", action="store_true",
                        help="show the stored documents and their document IDs")
    parser.add_argument("TERMS", nargs=argparse.REMAINDER,
                        help="terms to search for or add to the database")
    args = parser.parse_args()

    index = InvertedIndex()

    # If the database isn't where we expect it, then save a new one to disk.
    if not os.path.isfile(DB_FILE_NAME):
        print("Couldn't find the database, so a new one was created.")
        index.save_to_file(DB_FILE_NAME)

    try:
        index.load_from_file(DB_FILE_NAME)
        if args.add:
            if args.TERMS:
                add(index, args.TERMS)
            else:
                print("Provide a phrase to add, or run with -h for help")
        elif args.delete:
            delete(index, args.delete)
        elif args.show:
            show(index)
        else:
            if args.TERMS:
                search(index, args.TERMS)
            else:
                print("Provide terms to search for, or run with -h for help")
    except IOError:
        print("Hit a file-related error somewhere :(")


if __name__ == "__main__":
    main()
