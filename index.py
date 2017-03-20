#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Mar 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

First step for IR system implementation:
build an inverted index to search document collection.

'''
import os
import pickle
from collections import defaultdict

import re
# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


TREC8_PATH = 'TREC8all/Adhoc'
INDEX_PATH = 'index_TREC8'


class Index(object):
    '''
    Initialize the Index along with the preprocessing settings.

    lower <Bool> Set to True to lower-case all the tokens
    stem <Bool> Set to True to apply stemming to all the tokens
    lem <Bool> Set to True to apply lemmatization to all the tokens
    minToken <Int> Removes all the tokens with the length less than minToken
    '''
    def __init__(self, lower=True, stem=False, lem=True, minToken=4):
        self.inv_index = defaultdict(list)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lower = lower
        self.stem = stem
        self.lem = lem
        self.minToken = minToken

    def tokenize(self, s):
        '''
        Splits string into tokens, e.g. words.
        Remove punctuation.

        string <String> string to be tokenized
        '''
        # return string.split(' ')
        # return word_tokenize(s)
        return self.tokenizer.tokenize(s)

    def preprocess(self, tokens):
        '''
        Preprocess the input document text to normalize the vocabulary
        '''
        if self.lower:
            tokens = [token.lower() for token in tokens]
        if self.minToken:
            tokens = [token for token in tokens if len(token) >= self.minToken]
        # TODO stem and lem
        return tokens

    def load_collection(self, path, limit):
        '''
        Load document collection, e.g. CD4&5 of the TIPSTER collection.
        '''
        # counter for collection documents
        docid = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                if docid < limit:
                    with open(os.path.join(root, file), "r") as doc:
                        text = doc.read()
                        text = self.parse_trec(text)
                        docid += 1
                        self.create_inv_index(text, docid)

    def parse_trec(self, text):
        '''Removes XML tags from the document text'''
        return re.sub('<[^>]*>', '', text)

    def create_inv_index(self, text, docid):
        '''
        Builds an inverted index

        data <List> list of tokens to be indexed
        '''
        # for i, text in enumerate(docs):
        tokens = self.tokenize(text)
        tokens = self.preprocess(tokens)
        print 'Document', docid, ':', tokens[:10]
        for token in tokens:
            self.inv_index[token].append(docid)

    def store_inv_index(self, index_path):
        '''
        Store the inverted index.
        '''
        with open(index_path, 'wb') as f:
            pickle.dump(self.inv_index, f)

    def load_inv_index(self, index_path):
        '''
        Store the inverted index.
        '''
        with open(index_path, 'rb') as f:
            self.inv_index = pickle.load(f)

    def search(self, q):
        '''
        Search index
        '''
        pass

    def tfidf(self):
        pass

    def bm25(self):
        pass


if __name__ == '__main__':
    # use the index of the TREC8 collection
    index = Index()

    # load collection and store into index
    # index.load_collection(TREC8_PATH, limit=20)
    # index.store_inv_index(INDEX_PATH)

    # load index
    index.load_inv_index(INDEX_PATH)
    
    # print index.inv_index
