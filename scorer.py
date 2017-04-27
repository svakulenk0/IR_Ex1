#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Various weighting (scoring) functions for search

'''

import math
import numpy

from collections import Counter

from scipy.optimize import least_squares, minimize


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
        # print posting

        # calculate stats for the new term
        # process term stats: idfs, tfqw and k1
        if term not in self.idfs.keys():
            # print term
            self.idfs[term] = self.idf(posting['df'], n_docs)
            # compute only for BM25 weighting
            if isinstance(self, BM25) | isinstance(self, BM25_ADPT):
                # term frequency of the term in the query
                self.tfqw[term] = tfq / float(self.k3 + tfq)
                if isinstance(self, BM25_ADPT):
                # # # term frequency of the term in the query
                # # self.tfqw[term] = tfq / float(self.k3 + tfq)
                #     # calculate term-specific k1
                    self.k1[term] = self.estimate_k1(posting, n_docs)
                    # print term, self.k1[term]

        for docid, tf in posting.items():
            # skip non-document placeholder for df
            if docid == 'df':
                continue
                # print self.idfs[term]
            # add new document to the ranking
            if docid not in self.ranking.keys():
                # initial tfidf score for every document
                self.ranking[docid] = 0
                # compute only for BM25 weighting
                if isinstance(self, BM25) | isinstance(self, BM25_ADPT):
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
    name = 'tfidf'
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
    k1, k3 and b are the hyper-parameters
    '''
    name = 'bm25'

    def __init__(self, k3=1000, k1=1.2, b=0.75):
        # weighted term frequencies for each term in the query
        self.tfqw = {}
        self.k1 = k1
        self.b = b
        self.k3 = k3
        self.ldws = {}

    def calculate_score(self, tf, term, docid):
        '''
        '''
        # print self.tfqw[term]
        # weighted term frequencies for each term in the query
        # + document length compared to the average doc length
        return self.tfqw[term] * tf / (self.k1 * (1 - self.b + self.b * self.ldws[docid]) + tf) * self.idfs[term]


class BM25_ADPT(Scorer):
    '''
    Modified BM25 formula as described in the article Yuanhua Lv and Cheng Xiang Zhai. Adaptive Term Frequency Normalization for BM25. CIKM 2011
    (http: //sifaka.cs.uiuc.edu/~ylv2/pub/cikm11-adptTF.pdf)
    k3 and b are the hyper-parameters
    k1 is estimated on-line
    '''

    name = 'bm25_adpt'

    def __init__(self, k3=1000, b=0.75):
        # weighted term frequencies for each term in the query
        self.tfqw = {}
        # term-specific k1
        self.k1 = {}
        # self.k1 = {}
        self.b = b
        self.k3 = k3
        self.ldws = {}

    def info_gain(self, dft_1, dft, df, n_docs):
        '''
        calculate information gain
        '''
        # print (float(dft_1 + 0.5) / (dft + 1))
        # print (float(df + 0.5) / (n_docs + 1))
        return math.log((float(dft_1 + 0.5) / (dft + 1)), 2) - math.log((float(df + 0.5) / (n_docs + 1)), 2)

    def k1_fit(self, k1, i, ig):
        return ig - (k1 + 1) * i / (k1 + i)

    def estimate_k1(self, posting, n_docs):
        # for docid, tf in posting.items():
        # tfs = dict(posting)
        # print posting
        df = posting['df']
        del posting['df']
        dfts = Counter(posting.values())
        # print dfts
        # print dfts.keys()
        k1_sum = 0
        # print dfts[2], dfts[1], df, n_docs
        ig1 = self.info_gain(dfts[2], dfts[1], df, n_docs)
        # print ig1
        i_s = []
        igs = []
        for i in range(0, max(dfts.keys())+1):
            # print i
            # print dfts[i+1], dfts[i]
            igt = self.info_gain(dfts[i+1], dfts[i], df, n_docs)
            # print igt / ig1 - (k1 + 1) * i / (k1 + 1)
            i_s.append(i)
            igs.append(igt/ig1)
        out = least_squares(self.k1_fit, 1.2, args=(numpy.array(i_s), numpy.array(igs)))
        return out.x[0]

    def calculate_score(self, tf, term, docid):
        '''
        '''
        return self.tfqw[term] * tf / (self.k1[term] * (1 - self.b + self.b * self.ldws[docid]) + tf) * self.idfs[term]
        # return self.tfqw[term] * tf / (self.k1[term] * (1 - self.b + self.b * self.ldws[docid]) + tf) * self.idfs[term]
