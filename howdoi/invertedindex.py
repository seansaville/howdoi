"""
Module containing an implementation of an inverted index.
"""

import json

class InvertedIndex(object):
    """
    Inverted Index data structure.
    """

    """
    Words with no significant meaning in search queries which we therefore don't
    store in an inverted index.
    """
    stop_words = [
        'i', 'a', 'about', 'an', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
        'how', 'in', 'is', 'it', 'of', 'on', 'or', 'that', 'the', 'this', 'to',
        'was', 'what', 'when', 'where', 'which', 'who', 'will', 'with'
    ]


    def __init__(self):
        """
        index - a dictionary of postings lists (mappings of a term to the IDs of
                the documents it appears in)

        documents - a dictionary mapping document IDs to the documents
                    themselves

        next_doc_id - the next available document ID
        """

        self.index = {}
        self.documents = {}
        self.next_doc_id = 0


    def add_document(self, document, extra_tags):
        """
        Add a document to the inverted index. Tags it with each word in the
        query, and optionally with the provided extra tags.
        """

        # Add the document to the document store mapping IDs to documents
        doc_id = self.next_doc_id
        self.documents[doc_id] = document
        self.next_doc_id += 1

        # Add each occurrence of a term to its postings list (and create a list
        # if it doesn't exist). Treat the extra tags as if they were just
        # additional terms.
        terms = document.split(" ")
        terms.extend(extra_tags)
        for term in terms:
            if term not in InvertedIndex.stop_words:
                term = term.lower()
                if term not in self.index:
                    self.index[term] = []
                self.index[term].append(doc_id)


    def load_from_file(self, file_name):
        """
        Load an inverted index from a file.
        """

        with open(file_name, 'r') as input_file:
            in_dict = json.loads(input_file.readline())
            self.index = json.loads(in_dict['index'])
            self.documents = json.loads(in_dict['documents'])
            self.next_doc_id = json.loads(in_dict['next_doc_id'])


    def save_to_file(self, file_name):
        """
        Save the contents of this inverted index to a file.
        """

        with open(file_name, 'w') as output_file:
            out_dict = {}
            out_dict['index'] = json.dumps(self.index)
            out_dict['documents'] = json.dumps(self.documents)
            out_dict['next_doc_id'] = json.dumps(self.next_doc_id)
            output_file.write(json.dumps(out_dict))


    def search(self, tags):
        """
        Naive search. Finds the postings list for each tag and intersects them,
        returning the IDs of the documents that are in all of the lists.
        """

        postings_lists = []
        for tag in tags:
            tag = tag.lower()
            if tag in self.index:
                postings_lists.append(self.index[tag])

        if not postings_lists:
            return []

        matches = set(postings_lists[0])
        for postings_list in postings_lists:
            matches = matches.intersection(postings_list)

        return matches
