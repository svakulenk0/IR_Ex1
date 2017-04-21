#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Mar 20, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Unittests for Index class

'''

import unittest

import settings
from index import Index
from vectorize import VSM


DOCS = ["""Niners head coach Mike Singletary will let Alex Smith remain his starting 
        quarterback, but his vote of confidence is anything but a long-term mandate.
        Smith now will work on a week-to-week basis, because Singletary has voided 
        his year-long lease on the job.
        "I think from this point on, you have to do what's best for the football team,"
        Singletary said Monday, one day after threatening to bench Smith during a 
        27-24 loss to the visiting Eagles.
        """
        ,
        """The fifth edition of West Coast Green, a conference focusing on "green" home 
        innovations and products, rolled into San Francisco's Fort Mason last week 
        intent, per usual, on making our living spaces more environmentally friendly 
        - one used-tire house at a time.
        To that end, there were presentations on topics such as water efficiency and 
        the burgeoning future of Net Zero-rated buildings that consume no energy and 
        produce no carbon emissions.
        """
        ]

class TestIndex(unittest.TestCase):
    def test_create_inv_index(self):
        index = Index()
        index.parse_strings(DOCS)
        # print index.inv_index
        assert 'coach' in index.inv_index

    def test_create_index(self):
        index = Index()
        index.load_collection(settings.TREC8_PATH, limit=2)


class TestVSM():
    def test_vectorize(self):
        vsm = VSM(DOCS)

if __name__ == '__main__':
    unittest.main()
