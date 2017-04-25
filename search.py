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

'''
import settings
from trec_parser import parse_topics
from index import Index
from scorer import TFIDF, BM25


def search_trec(scorer):
    # parse topics/queries
    topics = parse_topics(settings.TREC8_TOPICS_PATH)
    # print topics
    # load inverted index
    index = Index(settings.INDEX_PATH, settings.LENGTH_PATH)
    # print index.inv_index
    assert 'N_DOCS' in index.inv_index
    print index.inv_index['N_DOCS'], "docs in the index"
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


if __name__ == '__main__':
    # scorer = TFIDF()
    scorer = BM25()
    search_trec(scorer)