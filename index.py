#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Mar 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

First step for IR system implementation:
build an inverted index to search document collection.

'''

from collections import defaultdict

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


class Index(object):
    ''''''
    def __init__(self):
        self.inv_index = defaultdict(list)
        self.tokenizer = RegexpTokenizer(r'\w+')

    def tokenize(self, s):
        '''
        Splits string into tokens, e.g. words.
        Remove punctuation.

        string <String> string to be tokenized
        '''
        # return string.split(' ')
        # return word_tokenize(s)
        return self.tokenizer.tokenize(s)

    def preprocess(self, tokens, stem=False, lem=True, trigrams=False):
        '''
        Preprocess the input document text.

        stem <Bool> Set to True to apply stemming to all the tokens
        lem <Bool> Set to True to apply lemmatization to all the tokens
        trigrams <Bool> Set to True to remove uni-, bi- and tri-grams from the tokens
        '''
        tokens = [token.lower() for token in tokens]
        if not trigrams:
            tokens = [token for token in tokens if len(token) > 3]
        # TODO stem and lem
        return tokens

    def create_inv_index(self, docs):
        '''
        Builds an inverted index

        data <List> list of tokens to be indexed
        '''
        for i, text in enumerate(docs):
            tokens = self.tokenize(text)
            tokens = self.preprocess(tokens)
            print tokens
            for token in tokens:
                self.inv_index[token].append(i)

# load document collection CD4&5 of the TIPSTER collection: TREC8Adhoc.tar.bz2
# Normalize the vocabulary


