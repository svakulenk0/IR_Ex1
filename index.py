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
import argparse

import pickle
from collections import defaultdict, Counter
import operator

import re
# from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer

import settings
from scorer import TFIDF
from trec_parser import parse_trec_doc


class Index(object):
    '''
    Initialize the Index along with the preprocessing settings.

    lower <Bool> Set to True to lower-case all the tokens
    stem <Bool> Set to True to apply stemming to all the tokens
    lem <Bool> Set to True to apply lemmatization to all the tokens
    minToken <Int> Removes all the tokens with the length less than minToken
    '''
    def __init__(self, index_path=False, length_path=False, lower=True, stem=False,
                 lem=True, minToken=4, removeStopwords=True):
        self.index = defaultdict(list)
        self.tokenizer = RegexpTokenizer(r'\w+')  # word-level tokenizer
        self.lower = lower
        if stem:
            self.stemmer = LancasterStemmer()
        elif lem:
            self.lemmatizer = WordNetLemmatizer()
        self.lem = lem
        self.stem = stem
        self.minToken = minToken
        self.removeStopwords = removeStopwords
        # load pre-constructed index
        if index_path:
            self.inv_index = self.load_dict(index_path)
        else:
            self.inv_index = defaultdict(list)
        if length_path:
            self.lds = self.load_dict(length_path)
        else:
            self.lds = defaultdict(list)

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
        if self.removeStopwords:
            tokens = [token for token in tokens if token not in stopwords.words('english')]
        if self.stem:
            tokens = [self.stemmer.stem(token) for token in tokens]
        elif self.lem:
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
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
        # make sure all documents are processed and stored in both data structures
        assert self.docid == len(self.lds)
        self.lds['AVG_LD'] = sum([ld for ld in self.lds.values()])/self.docid
        # print self.inv_index

    def load_collection(self, path, limit, inverted=True):
        '''
        Load document collection, e.g. CD4&5 of the TIPSTER collection.
        '''
        for root, dirs, files in os.walk(path):
            for file in files:
                
                with open(os.path.join(root, file), "r") as doc:
                    xml = doc.read()
                    try:
                        docs = parse_trec_doc(xml)
                        for docno, text in docs:
                            self.docid += 1
                            self.add_to_index(text, docno, inverted=True)
                            if limit and self.docid >= limit:
                                return
                    except:
                        continue

    def parse_xml(self, text):
        '''
        Basic XML clean up:
        Removes tags from the document text
        '''
        return re.sub('<[^>]*>', '', text)

    def parse_strings(self, list_of_strings):
        for string in list_of_strings:
            self.docid += 1
            self.add_to_index(string, self.docid)
       
    def add_to_index(self, text, docno, inverted=True):
        '''
        Builds an inverted index with tf(t,d) = f(t,d)
        '''
        # for i, text in enumerate(docs):
        tokens = self.tokenize(text)
        # maintain dictionary with the length of documents
        # length of the document = number of tokens
        self.lds[docno] = len(tokens)
        token_counts = self.preprocess(tokens)
        # print 'Document', self.docid, 'representation :', token_counts.most_common(3)
        print 'Document', docno, 'representation :', token_counts.most_common(3)
        if inverted:
            for token, count in token_counts.items():
                if token not in self.inv_index:
                    self.inv_index[token] = {}
                # tf = f
                self.inv_index[token][docno] = count
        else:
            self.index[docno] = tokens

    def df(self):
        '''
        Calculate and store document frequencies for each term at 'df' indices in the iverted index.
        '''
        for token, doc_tfs in self.inv_index.items():
            # print doc_tfs
            # self.inv_index[token]['df'] = sum([tf for doc, tf in doc_tfs.items()])
            # number of docs in which the term appears
            self.inv_index[token]['df'] = len(self.inv_index[token])

    def store_dict(self, path, dictionary):
        '''
        Store data on disk
        '''
        with open(path, 'wb') as f:
            pickle.dump(dictionary, f)

    def load_dict(self, path):
        '''
        Load data from disk
        '''
        dictionary = {}
        with open(path, 'rb') as f:
            dictionary = pickle.load(f)
        # print dictionary
        return dictionary

    # def search(self, query, scorer, AND=False):
    def search_topics(self, topic_path):
        parse_topics(topic_path)
        # self.search(query, scorer)

    def search(self, query, scorer, AND=False):
        '''
        Method to search documents in the inverted index
        given a query: 
        1) return all the documents where the query terms appear (with the OR operator)
        2) rank each of the docs using the chosen weighting scheme
        
        Input:

        query <String>
        scorer <Object> TFIDF or BM2b

        Output:

        returns document ranking sorted by the score

        '''
        # preprocessing
        tokens = self.tokenize(query)
        # counter for the term frequency of the term in the query
        terms = self.preprocess(tokens)
        # print terms
        # find a set of documents for each word in the query
        # doc_has_term = [(self.inv_index[term], term) for term in terms]
        # print doc_has_term
        # initialize the ranking
        scorer.ranking = {}
        # interate over terms in the query
        for term, tfq in terms.items():
            # print term
            # skip terms that are not indexed
            if term in self.inv_index.keys():
                # scorer.weight(term, [], self.inv_index['N_DOCS'])
                # print self.inv_index[term]
                # term posting tfq ndocs
                scorer.rank_docs(term, self.inv_index[term], tfq, self.inv_index['N_DOCS'], self.lds)
        # return document ranking sorted by the score
        return sorted(scorer.ranking.items(), key=operator.itemgetter(1), reverse=True)

        # answer_set = set(doc_has_word[0][0])

        # for d, w in doc_has_word:
        #     # AND query scenario
        #     if AND:
        #         answer_set = answer_set & set(d)
        #     # OR query
        #     else:
        #         answer_set = answer_set | set(d)
        # return answer_set


def parse_trec8(path=settings.TREC8_DOCS_PATH, limit=None, low=True, stem=False,
                lem=True, minchar=4, stopw=True):
    # create new index of the TREC8 collection
    index = Index(lower=low, stem=stem, lem=lem, minToken=minchar, removeStopwords=stopw)
    # load collection and store into index
    index.create_index(path, limit)
    # index.create_index(path=settings.TREC8_DOCS_PATH + '/latimes', limit=limit)
    # index.create_index(path=settings.TREC8_DOCS_PATH + '/fbis', limit=limit)
    # index.create_index(path=settings.TREC8_DOCS_PATH + '/ft', limit=limit)
    # index.create_index(path=settings.TREC8_DOCS_PATH + '/fr94', limit=limit)
    index.store_dict(settings.INDEX_PATH, index.inv_index)
    index.store_dict(settings.LENGTH_PATH, index.lds)


if __name__ == '__main__':
    # parse_trec8(limit=200)
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-path', type=str, default=settings.TREC8_DOCS_PATH,
                        help='specify path the document collection')
    parser.add_argument('-lim', type=str, default='None',
                        help='restrict the number of files to index for testing purposes, e.g. 200')
    parser.add_argument('-low', type=settings.str2bool, default=True,
                        help='lowercase')
    parser.add_argument('-stem', type=settings.str2bool, default=False,
                        help='apply stemming')
    parser.add_argument('-lem', type=settings.str2bool, default=True,
                        help='apply lemmatization')
    parser.add_argument('-minchar', type=int, default=4,
                        help='remove words with the number of characters less than MINCHAR')
    parser.add_argument('-stopw', type=settings.str2bool, default=True,
                        help='remove stopwords from the nltk list')

    args = parser.parse_args()
    print "Indexing parameters:", args
    if args.lim != 'None':
        args.lim = int(args.lim)
    parse_trec8(args.path, args.lim, args.low, args.stem, args.lem, args.minchar, args.stopw)
