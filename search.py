#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 25, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Search document collection.

For each topic of the 50 provided, the result should be a ranked list of up to 1000 documents, where each line is in the following format:

{topic-id} Q0 {document-id} {rank} {score} {run-name}

where

topic-id is an integer number between 401 and 450;

document-id is an identifier for the document (e.g. LA122690-0033);

Q0 unnecessary but must be present;

rank is an integer indicating the rank of the object in the sorted list (normally, this should be ascending from the first line to the last line)

score the similarity score calculated by (it has to not exceed the float precision and normally, this should be descending from the first line to the last line)

run-name a name you give to your experiment (free to choose)

Here is a short example of a potential output for all the topics:

401 Q0 FBIS3-10899 1 2.813525 grp5-exp1
401 Q0 FBIS3-13322 2 1.0114759 grp5-exp1
...
450 Q0 LA043089-0083 1000 0.08848727 grp5-exp1

command line interface (CLI): provide search parameters and a file with a topic to search for.


'''
import argparse

import settings
from trec_parser import parse_topics
from index import Index
from scorer import TFIDF, BM25, BM25_ADPT


def search_trec(scorer, top=1000, topic_limit=-1):
    '''
    top <int> number of best scored docs returned
    '''
    # parse topics/queries
    topics = parse_topics(settings.TREC8_TOPICS_PATH)  #[:topic_limit]
    # print topics
    # load inverted index
    index = Index(settings.INDEX_PATH, settings.LENGTH_PATH)
    # print index.inv_index
    assert 'N_DOCS' in index.inv_index
    # print "Indexed:", index.inv_index['N_DOCS'], "docs"
    assert index.inv_index['N_DOCS'] == len(index.lds) - 1
    assert 'AVG_LD' in index.lds
    # print "Average document length:", index.lds['AVG_LD']

    # search index
    # define weighting function
    # print scorer.name
    for desc, meta in topics:
        # print desc
        topicid = meta['qid']
        ranking = index.search(desc, scorer)
        
        # print ranking
        rank = 1
        for docid, score in ranking:
            print "{} Q0 {} {} {} {}".format(topicid, docid, rank, score, scorer.name)
            rank += 1
            if rank > top:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-scorer', type=str, default='tfidf',
                        help='specify scoring function to use: tfidf, bm25 or bm25adpt')
    # parser.add_argument('-lim', type=str, default='None',
    #                     help='restrict the number of topics (queries) for testing purposes, e.g. 2')
    parser.add_argument('-top', type=int, default=1000,
                        help='number of the top ranked documents to return for each of the topics')
    # parser.add_argument('-stem', type=settings.str2bool, default=False,
    #                     help='apply stemming')
    # parser.add_argument('-lem', type=settings.str2bool, default=True,
    #                     help='apply lemmatization')
    # parser.add_argument('-minchar', type=int, default=4,
    #                     help='remove words with the number of characters less than MINCHAR')
    # parser.add_argument('-stopw', type=settings.str2bool, default=True,
    #                     help='remove stopwords from the nltk list')

    args = parser.parse_args()
    print "Search parameters:", args
    scorer_string = args.scorer.lower()
    if scorer_string == 'tfidf':
        scorer = TFIDF()
    elif scorer_string == 'bm25':
        scorer = BM25()
    elif scorer_string == 'bm25adpt':
        scorer = BM25_ADPT()
    search_trec(scorer, args.top)