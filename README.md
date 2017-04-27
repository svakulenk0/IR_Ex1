Exercise 1.6 - TF-IDF, BM25 & BM25 ADPT, and evaluation (100/100 points)

Advanced Information Retrieval 2017S

# Goals:

* understanding of the practical issues of creating an inverted index for information retrieval

* implement basic scoring

* comprehend and apply advance scoring functions from research papers.

# Tasks: 

(1) index and search

(2) create a scorer that implements both TF-IDF and BM25 scoring functions

(3) implement the change to BM25 as described in [Yuanhua Lv and Cheng Xiang Zhai. Adaptive Term Frequency Normalization for BM25. CIKM 2011](http: //sifaka.cs.uiuc.edu/~ylv2/pub/cikm11-adptTF.pdf)

[Arjien P. de Vries et al. SIGIR 2005](http://homepages.cwi.nl/~arjen/pub/f330-devries.pdf)

(4) evaluate your results using the CD4&5 of the TIPSTER collection dataset provided and [the trec eval program](https://github.com/usnistgov/trec_eval).

(5) write a short report (upload everything to TUWEL, and present your results in person).

Deadline: Th, 27. April 2017, 23:55


## Index

Build an inverted index from the document collection CD4&5 of the TIPSTER collection as provided on the link here and in TUWEL: TREC8Adhoc.tar.bz2

Normalize the vocabulary by applying any combination of the techniques described in Chapter 2 of the Introduction to Information Retrieval book (case folding, removing stop-words, stemming, lemmatization).

These options should be exposed as parameters in the index creation phase. 

You should provide an executable indexer.sh file that given the necessary parameters generates the required index.


## Search

Implement a basic search functionality and provide it as a command line interface (CLI): provide search parameters and a file with a topic to search for.

The system then returns a list of documents ranked by a similarity function of your choice and based on a variant of term frequency ranking. Different components (e.g. scoring function) need to be exposed as parameters in the command line.

TF-IDF and BM25 scoring methods have to be implemented.

The search engine must take as a parameter the topic file. You are provided with a set of 50 topics to search for. They are all in the dataset and have a simple SGML structure. Each topic is delimited by <TOP> tags and you are free to use all or part of their content in your search.

Implement topic processing and the actual scoring/ranking as two separate tasks.

By topic processing we understand here simply getting the terms that will be search in the index. Consider the use or not use of the different elements in the topic document.

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

You should provide an executable searcher.sh file that given the necessary parameters generates a ranked list as above.

Your task is to modify your implementation of the BM25 scoring function and create a new similarity class called BM25 ADPT, which adapts dynamically the parameter k1 of BM25. Repeat your search from above with BM25 and your newly implemented class as indicated in the evaluation section.

## Evaluation
You must use trec eval to calculate the Mean Average Precision (MAP) of your result lists over the 50 topics provided. trec eval is a small C application, you have to compile it for your machine. In principle, you can use any C compiler (most Linux distributions already come with one), and just run the make command in the folder2.

$trec_eval -q -m map -c qrels_file your_results_file

where the parameters are:
-m measure: Add ’measure’ to the lists of measures to calculate and print. If ’measure’ contains a ’.’, then the name of the measure is everything preceding the period, and everything to the right of the period is assumed to be a list of parameters for the measure, separated by ’,’. There can be multiple occurrences of the -m flag. ’measure’ can also be a nickname for a set of measures. 

Current nicknames include
’official’ : the main measures often used by TREC
’all trec’ : all measures calculated with the standard TREC results and rel info format
files.
’set’ : subset of all trec that calculates unranked values.
’prefs’ : Measures not in all trec that calculate preference measures.

-c: Average over the complete set of queries in the relevance judgements instead of the queries in the intersection of relevance judgements and results. Missing queries will contribute a value of 0 to all evaluation measures (which may or may not be reasonable for a particular evaluation measure, but is reasonable for standard TREC measures.) Default is off.

-q: In addition to summary evaluation, give evaluation for each query/topic
and where

qrels file is the file available on the resources on TUWEL.

your results file is your results file using the format indicated above, where all topics are present.

In the end, your results should be in a table.

## Report

Describe briefly your index, in particular which additional information is required to be saved, if any. Show how the score is calculated for two documents adjacent in the ranked list. For this, you may use a query of your choosing (the simpler the query, the simpler the explanation, but you must have at least two terms in the query).

Finally, show your MAP results calculated using trec eval. Try to find a justification of why a retrieval model performed better than the other. 

Explain how to run the prototype. 

Maximum size: 4 pages or 2000 words.


## Hand-in Presentation

General knowledge about the system (e.g. what a tokenizer is, which stemmer have you used, how to change it, how to change the scoring function, what are the language-specific features).

• Final deadline is April 28th: upload a zipped file to TUWEL (report, source code, and corresponding executable jar file incl. all dependencies);

• Lab locations are on TISS.

Note: 35 points to pass the course.



# Implementation

## Dependencies

* nltk, download corpora/stopwords and wordnet resources:

python 
import nltk
nltk.download()
d
stopwords
wordnet

http://blog.nlpapi.co/how-to-install-nltk-corporastopwords/

## Usage:

1. Download and unzip the TREC-8 collection:

lswget *URL-of-the-dataset*
unzip TREC8all.zip
tar xvjf TREC8Adhoc.tar.bz2

2. Run unittests: python tests.py

3. Index the TREC-8 collection: python index.py

4. Search topics in the index:

python search.py > ./results/results_tfidf
python search.py > ./results/results_bm25
python search.py > ./results/results_bm25_adpt

# Results

1st run
Indexed: 211,349 docs

2nd run (improved parsing: partial fix for 2 folders):
Indexed: 266,979 docs

## Errors (TODO)

* Parsing:
Document LA122590-0120 representation : []


# References


* Inverted Index Python implementation(https://github.com/willf/inverted_index)

* [Python: Inverted Index for dummies](http://th30z.blogspot.co.at/2010/10/python-inverted-index-for-dummies.html)(https://github.com/matteobertozzi/blog-code/blob/master/py-inverted-index/invindex.py)

* (http://www.nltk.org/_modules/nltk/tokenize.html)

* [Least-squares fitting in Python](https://python4mpia.github.io/fitting_data/least-squares-fitting.html)

* [Argbash online: generate script](https://argbash.io/generate)

* [Stemming and Lemmatization with Python NLTK](http://text-processing.com/demo/stem/)