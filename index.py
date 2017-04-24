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
from collections import defaultdict, Counter

import re
# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

import settings
from scorer import TFIDF


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
        self.tokenizer = RegexpTokenizer(r'\w+')  # word-level tokenizer
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

        returns token counter (dictionary with counts for each token)
        '''
        if self.lower:
            tokens = [token.lower() for token in tokens]
        if self.minToken:
            tokens = [token for token in tokens if len(token) >= self.minToken]
        # TODO stem and lem ?
        return Counter(tokens)

    def create_index(self, path=None, limit=None, list_of_strings=None):
        # counter for documents
        self.docid = 0
        if path:
            self.load_collection(path, limit, inverted=True)
        else:
            self.parse_strings(list_of_strings)
        # calculate document frequencies for each term in inverted index
        self.df()
        # store the number of docs in the collection N
        self.inv_index['N_DOCS'] = self.docid
        # print self.inv_index

    def load_collection(self, path, limit, inverted=True):
        '''
        Load document collection, e.g. CD4&5 of the TIPSTER collection.
        '''
        for root, dirs, files in os.walk(path):
            for file in files:
                if self.docid < limit:
                    with open(os.path.join(root, file), "r") as doc:
                        text = doc.read()
                        text = self.parse_trec(text)
                        self.docid += 1
                        self.add_to_index(text, inverted=True)

    def parse_trec(self, text):
        '''Removes XML tags from the document text'''
        return re.sub('<[^>]*>', '', text)

    def parse_strings(self, list_of_strings):
        for string in list_of_strings:
            self.docid += 1
            self.add_to_index(string)
       
    def add_to_index(self, text, inverted=True):
        '''
        Builds an inverted index with tf(t,d) = f(t,d)
        '''
        # for i, text in enumerate(docs):
        tokens = self.tokenize(text)
        token_counts = self.preprocess(tokens)
        print 'Document', self.docid, 'representation :', token_counts
        if inverted:
            for token, count in token_counts.items():
                if token not in self.inv_index:
                    self.inv_index[token] = {}
                # tf = f
                self.inv_index[token][self.docid] = count
        else:
            self.index[self.docid] = tokens

    def df(self):
        '''
        Calculate and store document frequencies for each term at 'df' indices in the iverted index.
        '''
        for token, doc_tfs in self.inv_index.items():
            print doc_tfs
            self.inv_index[token]['df'] = sum([tf for doc, tf in doc_tfs.items()])

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

    def search(self, query, AND=False):
        '''
        Method to search documents in the inverted index
        given a query: 
        1) return all the documents where the query terms appear (with the OR operator)
        2) rank each of the docs using the chosen weighting scheme
        query <String>
        '''
        # preprocessing
        tokens = self.tokenize(query)
        terms = self.preprocess(tokens)

        # find a set of documents for each word in the query
        # doc_has_term = [(self.inv_index[term], term) for term in terms]
        # print doc_has_term

        scorer = TFIDF()
        for term in terms:
            print term
            # skip terms that are not indexed
            if term in self.inv_index.keys():
                # scorer.weight(term, [], self.inv_index['N_DOCS'])
                print self.inv_index[term]
                scorer.weight(term, self.inv_index[term], self.inv_index['N_DOCS'])
        return scorer.ranking

        # answer_set = set(doc_has_word[0][0])

        # for d, w in doc_has_word:
        #     # AND query scenario
        #     if AND:
        #         answer_set = answer_set & set(d)
        #     # OR query
        #     else:
        #         answer_set = answer_set | set(d)
        # return answer_set


def parse_trec8():
    # create new index of the TREC8 collection
    index = Index()
    # load collection and store into index
    index.create_index(path=settings.TREC8_PATH, limit=20)
    index.store_inv_index(settings.INDEX_PATH)


if __name__ == '__main__':
    pass
