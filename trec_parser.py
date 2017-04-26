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


def parse_trec_doc(xml):
    # clean
    xml = re.sub('<!--[^>]*-->', '', xml).strip()
    xml = re.sub('&[^>]*;', ' ', xml).strip()
    # print xml
    xml = '<ROOT>' + xml + '</ROOT>'   # Let's add a root tag
    root = ET.fromstringlist(xml)
    # print root
    # print root.findall('DOC')
    docs = []
    for doc in root:
        # for child in doc:
            # print child.tag)
        text = doc.find('TEXT').text.strip()
        # print doc.find('DOCNO').text.strip()
        # print text

        if not text:
            if doc.find('TEXT').find('P'):
                paragraphs = []
                for p in doc.find('TEXT').findall('P'):
                    paragraphs.append(p.text.strip())
                text = '\n'.join(paragraphs)
            elif doc.find('TEXT').findall('SUMMARY'):
                text = doc.find('TEXT').find('SUMMARY').text.strip() 
        docs.append((doc.find('DOCNO').text.strip(), text))
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
    fileid = 0
    for root, dirs, files in os.walk(doc_path):
        for file in files:
            print file
            # tree = ET.parse(os.path.join(root, file))
            with open(os.path.join(root, file), "r") as doc:
                text = doc.read()
                try:
                    fileid += 1
                    if fileid >= limit:
                        print fileid, "files processed"
                        return
                    print parse_trec_doc(text)
                except:
                    continue
    print fileid, "files processed"


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
    parse_trec_docs(settings.TREC8_DOCS_PATH + '/fr94', limit=2)
    # parse_trec_docs(settings.TREC8_DOCS_PATH + '/latimes', limit=2)
    # parse_trec_docs(settings.TREC8_DOCS_PATH + '/ft', limit=2)
    # parse_trec_docs(settings.TREC8_DOCS_PATH + '/fbis', limit=2)
    # print parse_topics(settings.TREC8_TOPICS_PATH)