#!/usr/bin/python3

"""
howdoi

Search a database of small pieces of information and output the results in the
terminal.
"""

import json


class InvertedIndex(object):
    """
    Inverted Index data structure.
    """

    def __init__(self):
        """
        index - a dictionary of postings lists (mappings of a term to the IDs of
                the documents it appears in)

        term_dict - a dictionary mapping document IDs to the documents
                    themselves
        """

        self.index = {}
        self.term_dict = {}
        self.next_doc_id = 0


    def add_document(self, document):
        """
        Add a document to the inverted index.
        """

        # Add the document to the document store mapping IDs to documents
        doc_id = self.next_doc_id
        self.term_dict[doc_id] = document
        self.next_doc_id += 1

        # Add each term to the postings list for that term (and create one if
        # it doesn't exist)
        terms = document.split(" ")
        for term in terms:
            if term not in self.index:
                self.index[term] = []
            self.index[term].append(doc_id)


    def load_file(self, file_name):
        """
        Load an inverted index from a file.
        """

        with open(file_name, 'r') as input_file:
            in_dict = json.loads(input_file.readline())
            self.index = json.loads(in_dict['index'])
            self.term_dict = json.loads(in_dict['term_dict'])
            self.next_doc_id = json.loads(in_dict['next_doc_id'])


    def save_file(self, file_name):
        """
        Save the contents of this inverted index to a file.
        """

        with open(file_name, 'w') as output_file:
            out_dict = {}
            out_dict['index'] = json.dumps(self.index)
            out_dict['term_dict'] = json.dumps(self.term_dict)
            out_dict['next_doc_id'] = json.dumps(self.next_doc_id)
            output_file.write(json.dumps(out_dict))
