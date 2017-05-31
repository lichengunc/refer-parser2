# refer-parser2
Referring Expression Parser


## Introduction
Our parser provides functions of
* find the head noun word of a sentence
* find the 7 attribute words as ReferitGame paper
* find all noun words given a sentence
* parse one sentence
* parse batch of sentences using multi-threads
* check if two sentences share same head word
* check if two sentences share similar noun words

## Requirements
This code is written in python and requires several libraries.
```bash
gensim
nltk
corenlp
```
We prune the core part of corenlp-python in this repository, whose original git can be downloaded [here](https://bitbucket.org/jeremybmerrill/corenlp-python.git). 
Note this (our) corenlp is able to read [v3.5.1](http://nlp.stanford.edu/software/stanford-corenlp-full-2015-01-29.zip) and [v3.5.2](http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip), but not able to load V3.6.0. 
Also note Stanford NLP group switches to Universal Dependencies standard since v3.5.2.

In order to compute word similarities and word representation, we need to download pretrained GoogleNews 300-D word2vec model from this [website](https://code.google.com/archive/p/word2vec/), and then use [Gensim](https://radimrehurek.com/gensim/models/word2vec.html) to load it.

## Pretrained Models
We will use two pretrained models and save them into ``./model`` folder. 
They are [corenlp v3.5.2](http://nlp.stanford.edu/software/stanford-corenlp-full-2015-04-20.zip) and [GoogleNews-vectors-negative300.bin](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing) separately.
Before using the models, run ``unzip models/stanford-corenlp-full-2015-04-20.zip``

## Usage
Initialize refer parser.
```bash
ref_parser = REFER_PARSER(corenlp_model_path, word2vec_model_path)
```
If you want to use single model, need to further call
```bash
ref_parser.load_corenlp()  # for the use of parsing
ref_parser.load_word2vec()  # for the use of computeing word2vec
```

Given a bunch of sentences, return the list of parse results.
```bash
parse_results = ref_parser.parse_sents(sentences, num_workers=3)
```

### License
BSD License.

