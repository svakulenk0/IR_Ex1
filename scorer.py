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

    ranking = {}
    idfs = {}

    def weight(self):
        # no to be called directly but overloaded by subclasses
        raise NotImplementedError
    # calculated and stored within the inverted index already 
    # def tf(self, term, tokenized_document):
    #     return tokenized_document.count(term)

    def idf(self, df, n_docs):
        # add-one smoothing to avoid devision by 0 if there is no term in 
        # return math.log((1 + float(n_docs)) / (1 + df))
        return math.log(float(n_docs) / df)


class TFIDF(Scorer):
    '''
    tfidf scoring 
    '''
    def weight(self, term, posting, n_docs):
        # tfidf
        # if posting:
        for docid, tf in posting.items():
            # skip non-document placeholder for df
            if docid == 'df':
                continue
            if term not in self.idfs.keys():
                self.idfs[term] = self.idf(posting['df'], n_docs)
                # print self.idfs[term]
            if docid not in self.ranking.keys():
                # initial tfidf score for every document
                self.ranking[docid] = 0
            self.ranking[docid] += tf * self.idfs[term]
            # print self.ranking[docid]


class BM25(Scorer):
    '''
    '''

    def weight(self):
        pass

class NewBM25(Scorer):
    '''
    '''

    def weight(self):
        '''
        Modified BM25 formula as described in the article published by Arjien P. de Vries et al. 2005 at SIGIR
        (http://homepages.cwi.nl/~arjen/pub/f330-devries.pdf)
        '''
        pass

# if __name__ == '__main__':
    