#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 25, 2017

.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

Parse topic and documents files.
'''
import re
import os
import xml.etree.ElementTree as ET

import settings


def parse_trec_doc(text):
    # print text
    xml = '<ROOT>' + text + '</ROOT>'   # Let's add a root tag

    root = ET.fromstring(xml)
    docs = []
    for doc in root:
        # for child in doc:
            # print child.tag)
        docs.append((doc.find('DOCNO').text.strip(), doc.find('TEXT').text.strip()))
    return docs
            # print(
            #     'DOC NO: {}, HT: {}, HEADER: {}, TEXT: {}'.format( # Nice formatting py 3 \o/
            #         doc.find('DOCNO').text.strip(),
            #         doc.find('HT').text.strip(),
            #         doc.find('HEADER').text.strip(),
            #         doc.find('TEXT').text.strip(),
            #     )
            # )

def parse_trec_docs(doc_path, limit):
    fileid = 1
    for root, dirs, files in os.walk(doc_path):
        for file in files:
                # tree = ElementTree(file=os.path.join(root, file))
                # tree = ET.parse(os.path.join(root, file))
                with open(os.path.join(root, file), "r") as doc:
                    text = doc.read()
                    try:
                        parse_trec_doc(text)
                        fileid += 1
                        if fileid >= limit:
                            print fileid, "files processed"
                            return
                    except:
                        continue
    print "all", fileid, "files processed"


def parse_topics(topic_path):
    '''
    Adopted from https://github.com/rmit-ir/SummaryRank/blob/master/summaryrank/trec_novelty.py
    '''
    with open(topic_path, "r") as doc:
        """ Get TREC description topics. """
        result = []
        metadata = None
        tag = None
        for line in doc.readlines():
            if line.startswith('<'):
                if line.startswith('<top>'):
                    metadata = dict()
                    tag = None
                # SV fix
                elif line.startswith('<title>'):
                    # m = re.match(r'<title>\s*(\w+)*', line)
                    # assert m
                    metadata['title'] = line[8:]
                elif line.startswith('<num>'):
                    m = re.match(r'<num>\s*Number:\s*(\S+)', line)
                    assert m
                    metadata['qid'] = m.group(1)
                elif line.startswith('</top>'):
                    desc = metadata.get('desc', None)
                    result.append((' '.join([l.strip() for l in desc]).strip(), metadata))
                else:
                    m = re.match(r'<(.*?)>', line)
                    assert m
                    tag = m.group(1)
                    metadata[tag] = []
            elif tag:
                metadata[tag].append(line)

        return result


if __name__ == '__main__':
    parse_trec_docs(settings.TREC8_DOCS_PATH, limit=2)
    # print parse_topics(settings.TREC8_TOPICS_PATH)