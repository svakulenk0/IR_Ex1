#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

'''

# store shared variables here
TREC8_DOCS_PATH = 'TREC8all/Adhoc'
TREC8_TOPICS_PATH = 'TREC8all/topicsTREC8Adhoc.txt'
TEST_INDEX_PATH = 'test_index_TREC8'
INDEX_PATH = 'index_TREC8'
TEST_LENGTH_PATH = 'test_length_TREC8'
LENGTH_PATH = 'length_TREC8'

# shared method to convert strings to Python boolean type for argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
