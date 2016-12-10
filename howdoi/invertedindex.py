"""
Module containing an implementation of an inverted index.
"""

import json

class InvertedIndex(object):
    """
    Inverted index data structure.
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

        custom_tags - a dictionary mapping document IDs to their custom
                      (user-provided) search tags

        next_doc_id - the next available document ID
        """

        self.index = {}
        self.documents = {}
        self.custom_tags = {}
        self.next_doc_id = 0


    def add_document(self, document, custom_tags):
        """
        Add a document to the inverted index. Tags it with either each
        significant word in the document, or with the custom tags provided if
        custom_tags is nonempty.
        """

        # Add the document to the document store
        doc_id = self.next_doc_id
        self.documents[doc_id] = document
        self.next_doc_id += 1

        # Add the document ID to the postings list for each of its terms. if
        # custom tags were provided, use those instead.
        if not custom_tags:
            terms = document.split(" ")
        else:
            self.custom_tags[doc_id] = custom_tags
            terms = custom_tags

        for term in terms:
            if term not in InvertedIndex.stop_words:
                term = term.lower()
                # If a postings list for this term doesn't exist, create it.
                if term not in self.index:
                    self.index[term] = []
                self.index[term].append(doc_id)


    def delete_document(self, doc_id):
        """
        Delete a document from the inverted index. Returns True if the document
        existed and was deleted, False otherwise.
        """

        if doc_id in self.documents:
            # Remove the document ID from the postings list for all terms it
            # contains or is tagged with
            if doc_id in self.custom_tags:
                terms = self.custom_tags[doc_id]
            else:
                terms = self.documents[doc_id].split(" ")
            for term in terms:
                if term not in InvertedIndex.stop_words:
                    term = term.lower()
                    self.index[term].remove(int(doc_id))
                    # If the postings list is now empty, remove it
                    if not self.index[term]:
                        del self.index[term]

            # Remove the document from the document store
            del self.documents[doc_id]
            return True
        else:
            return False


    def load_from_file(self, file_name):
        """
        Load an inverted index from a file.
        """

        with open(file_name, 'r') as input_file:
            in_dict = json.loads(input_file.readline())
            self.index = json.loads(in_dict['index'])
            self.documents = json.loads(in_dict['documents'])
            self.custom_tags = json.loads(in_dict['custom_tags'])
            self.next_doc_id = json.loads(in_dict['next_doc_id'])


    def save_to_file(self, file_name):
        """
        Save the contents of this inverted index to a file.
        """

        with open(file_name, 'w') as output_file:
            out_dict = {}
            out_dict['index'] = json.dumps(self.index)
            out_dict['documents'] = json.dumps(self.documents)
            out_dict['custom_tags'] = json.dumps(self.custom_tags)
            out_dict['next_doc_id'] = json.dumps(self.next_doc_id)
            output_file.write(json.dumps(out_dict))


    def search(self, terms):
        """
        Naive search. Finds the postings lists for each search term and
        intersects them, returning the IDs of the documents that are in all of
        the lists.
        """

        postings_lists = []
        for term in terms:
            term = term.lower()
            if term not in InvertedIndex.stop_words:
                if term in self.index:
                    postings_lists.append(self.index[term])

        if not postings_lists:
            return []

        matches = set(postings_lists[0])
        for postings_list in postings_lists:
            matches = matches.intersection(postings_list)

        return matches
