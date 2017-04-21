#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Vector space model

'''
import numpy
from collections import Counter

import settings
from index import Index


class VSM(object):
    '''
    Vector space model
    '''

    def __init__(self, docs=False, collection_path=False, limit=-1):
        self.vocabulary = {}
        self.inv_vocabulary = {}
        self.collection = Index()
        if collection_path:
            # index collection
            self.collection.load_collection(collection_path, limit)
        elif docs:
            self.collection.parse_strings(docs)
        self.construct_vocabulary()
        self.vectorize_docs()

    def construct_vocabulary(self):
        """ create the keyword associated to the position of the elements within the document vectors """
        term_id = 0
        for term in self.collection.inv_index.keys():
            self.vocabulary[term] = term_id
            self.inv_vocabulary[term_id] = term
            term_id += 1

    # def save_vocabulary(self)
    # def vectorize_doc(document):
    #     '''
    #     returns a vector for the input document
    #     '''
    #     pass

    def vectorize_docs(self):
        '''
        returns a matrix with row-vectors for each of the input documents
        '''
        # initialize empty matrix in the size of the collection
        if not self.vocabulary:
            self.construct_vocabulary()
        # number of docs
        nrows = len(self.collection.index)
        print nrows, 'docs'
        # number of terms 
        ncolumns = len(self.vocabulary)
        print ncolumns, 'terms'
        # initialize tf matrix
        self.tf = numpy.zeros(shape=(nrows, ncolumns), dtype=numpy.int8)
        # print len(self.collection.index)
        for doc_id, terms in self.collection.index.items():
            # count terms
            tf = Counter(terms)
            for term in tf:
                self.tf[doc_id-1][self.vocabulary[term]] = tf[term]
        print self.tf


if __name__ == '__main__':
    # use the index of the TREC8 collection
    # trec8 = Index(settings.INDEX_PATH)
    vsm = VSM(collection_path=settings.TREC8_PATH, limit=2)
