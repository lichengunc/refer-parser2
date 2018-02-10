# refer-parser2
Referring Expression Parser


## Introduction
Our parser provides functions of
* parse sentences in multithread mode using StanfordNLP and SENNA
* find the head noun word of a sentence
* find the 7 attribute words as ReferitGame paper
* chunk sentences
* write htmls

## Requirements
This code is written in python and requires several libraries.
```bash
practnlptools
nltk
corenlp
unidecode
```
We prune the core part of corenlp-python in this repository, whose original git can be downloaded [here](https://bitbucket.org/jeremybmerrill/corenlp-python.git). 
Note this (our) corenlp is able to read [v3.5.1](http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip) and [v3.5.2](http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip), but not able to load V3.6.0. 
Also note Stanford NLP group switches to Universal Dependencies standard since v3.5.2.
We also use [SENNA](http://ronan.collobert.com/senna/)'s python wrapper, [practnlptools](https://pypi.python.org/pypi/practnlptools/1.0) to chunk each sentence into phrase structures.

## How to use
1a) Parse expressions using Stanford Parser:
```bash
python parse_sents.py --dataset refcoco --splitBy unc --num_workers 4
```
1b) Parse expressions using [Vicente's R1-R7 attributes](http://tamaraberg.com/papers/referit.pdf):
```bash
python parse_atts.py --dataset refcoco --splitBy unc
```
1c) Visualize decomposed attributes:
```bash
python write_att_html.py --dataset refcoco --splitBy unc
```

2a) Parse expression using SENNA parser:
```bash
python senna_sents.py --dataset refcoco --splitBy unc --num_workers 4
```
2b) Chunk expressions into phrase structures:
```bash
python chunk_sents.py --dataset refcoco --splitBy unc
```
2c) Analyze the phrase structures from the chunking results:
```bash
python analyze_chunk.py --dataset refcoco --splitBy unc
```
2d) Visualize the phrase structures:
```bash
python write_chunk_html.py --dataset refcoco --splitBy unc
```

## Download
* [**Parsed expressions**](http://bvision.cs.unc.edu/licheng/MattNet/refer-parser2/cache/parsed_atts.zip) using [Vicente's R1-R7 attributes](http://tamaraberg.com/papers/referit.pdf)

### License
BSD License.

