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

import settings


class Index(object):
    '''
    Initialize the Index along with the preprocessing settings.

    lower <Bool> Set to True to lower-case all the tokens
    stem <Bool> Set to True to apply stemming to all the tokens
    lem <Bool> Set to True to apply lemmatization to all the tokens
    minToken <Int> Removes all the tokens with the length less than minToken
    '''
    def __init__(self, index_path=False, lower=True, stem=False, lem=True, minToken=4):
        self.index = defaultdict(list)
        self.inv_index = defaultdict(list)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.lower = lower
        self.stem = stem
        self.lem = lem
        self.minToken = minToken
        # load pre-constructed index
        if index_path:
            self.load_inv_index(index_path)

    def tokenize(self, s):
        '''
        Splits string into tokens, e.g. words.
        Remove punctuation.

        string <String> string to be tokenized
        '''
        # return string.split(' ')
        # return word_tokenize(s)
        # print s
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

    def load_collection(self, path, limit, inverted=True):
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
                        self.create_index(text, docid, inverted=True)

    def parse_trec(self, text):
        '''Removes XML tags from the document text'''
        return re.sub('<[^>]*>', '', text)

    def parse_strings(self, list_of_strings):
        docid = 0
        for string in list_of_strings:
            docid += 1
            self.create_index(string, docid)

    def create_index(self, text, docid, inverted=True):
        '''
        Builds an inverted index
        '''
        # for i, text in enumerate(docs):
        tokens = self.tokenize(text)
        tokens = self.preprocess(tokens)
        print 'Document', docid, ':', tokens[:10]
        # bow model
        self.index[docid] = tokens
        if inverted:
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

    def search(self, query, AND=True):
        '''
        Method to search documents in the inverted index
        given a query

        query <String>
        '''
        # preprocessing
        tokens = self.tokenize(query)
        wordlist = self.preprocess(tokens)

        # find a set of documents for each word in the query
        doc_has_word = [ (self.inv_index[word], word) for word in wordlist ]
        print doc_has_word

        # if AND : AND query scenario
        # answer_set = set(doc_has_word[0][0])
        # for d, w in doc_has_word:
        #     answer_set = answer_set & set(d)

        # return answer_set


if __name__ == '__main__':
    # use the index of the TREC8 collection
    index = Index(settings.INDEX_PATH)

    # load collection and store into index
    # index.load_collection(settings.TREC8_PATH, limit=20)
    # index.store_inv_index(settings.INDEX_PATH)

    # search index
    query = 'medications 0947'  # answer: 1
    print index.search(query)
