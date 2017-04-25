#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Various weighting (scoring) functions for search

'''

import math


class Scorer(object):
    '''
    Abstract class for implementing different weighting (scoring) functions for search
    '''

    # def __init__(self):
    ranking = {}
    idfs = {}

    def rank_docs(self, term, posting, tfq, n_docs, lds):
        # no to be called directly but overloaded by subclasses
        # raise NotImplementedError
    # calculated and stored within the inverted index already 
    # def tf(self, term, tokenized_document):
    #     return tokenized_document.count(term)
        # if posting:
        for docid, tf in posting.items():
            # skip non-document placeholder for df
            if docid == 'df':
                continue
            # calculate stats for the new term
            if term not in self.idfs.keys():
                self.idfs[term] = self.idf(posting['df'], n_docs)
                # compute only for BM25 weighting
                if isinstance(self, BM25):
                    # term frequency of the term in the query
                    self.tfqw[term] = tfq / float(self.k2 + tfq)
                # print self.idfs[term]
            # add new document to the ranking
            if docid not in self.ranking.keys():
                # initial tfidf score for every document
                self.ranking[docid] = 0
                # compute only for BM25 weighting
                if isinstance(self, BM25):
                    self.ldws[docid] = lds[docid] / lds['AVG_LD']
            self.ranking[docid] += self.calculate_score(tf, term, docid)
            # print self.ranking[docid]

    def idf(self, df, n_docs):
        # smoothing to avoid devision by 0 if there is no term in 
        # return math.log(float(n_docs) / df)
        return math.log((n_docs - df + 0.5)/(df - 0.5))


class TFIDF(Scorer):
    '''
    tfidf scoring 
    '''
    # def __init__(self):

    def calculate_score(self, tf, term, *args):
        '''
        *args allows to pass any number of params to this method
        '''
        # tfidf
        # return round(tf * self.idfs[term], 2)
        return tf * self.idfs[term]


class BM25(Scorer):
    '''
    '''
    def __init__(self, k2=100, k1=1.2, b=0.75):
        # weighted term frequencies for each term in the query
        self.tfqw = {}
        self.k1 = k1
        self.b = b
        self.k2 = k2
        self.ldws = {}

    def calculate_score(self, tf, term, docid):
        '''
        k1, k2 and b are the hyper-parameters
        '''
        # print self.tfqw[term]
        return self.tfqw[term] * tf / (self.k1 * (1 - self.b + self.b * self.ldws[docid]) + tf) * self.idfs[term]


class NewBM25(BM25):
    '''
    Modified BM25 formula as described in the article published by Arjien P. de Vries et al. 2005 at SIGIR
    (http://homepages.cwi.nl/~arjen/pub/f330-devries.pdf)
    '''

    def weight(self):
        pass

# if __name__ == '__main__':
    