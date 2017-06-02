"""
This code will call pyutils/attparser to parse each sentence into 7 attributes.
The parser rule is according to Vicente's paper "Referit Game", EMNLP2014.
Specifically, r1 = entry-level name, r2 = color, r3 = size, r4 = abs. location,
r5 = rel. location, r6 = rel. object, r7 = generic, r8 = the left words

Before running this code, make sure you have already run parse_sents.py, whose output is
sents = [{sent_id, sent, parse, raw, tokens}]
The attparser will fetch the parse of each sent, then decompose it into 7 categories.

The output will be saved in 'cache/parsed_atts/dataset_splitBy/sents.json', where
sents = [{sent_id, sent, parse, raw, tokens, atts, left}]
"""
import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json
from pyutils.attparser import cocoParser, clefParser
# set nltk data path
import nltk
# nltk.data.path.append('/Users/liyu/Documents/nltk_data')
nltk.data.path.append('/mnt/ilcompf6d0/user/liyu/Developments/nltk_data')

def analyze(sents):
	# do some statistics
	usage = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0}
	for sent in sents:
		for r in usage:
			usage[r] = usage[r] + 1 if sent['atts'][r] != ['none'] else usage[r]
	for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']:
		usage[r] /= float(len(sents))
		print('Usage of %s is %.2f%%.' % (r, usage[r] * 100))

def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/parsed_atts/' + dataset_splitBy):
		os.makedirs('cache/parsed_atts/' + dataset_splitBy)

	# load parsed sents, where sents.json =
	# [{sent_id, sent, parse, raw, tokens}], where parse = {dependencies, parsetree, text, workds}
	path_to_parsed_sents = osp.join('cache/parsed_sents', dataset_splitBy, 'sents.json')
	sents = json.load(open(path_to_parsed_sents))

	# parse attributes for each sent
	if 'refcoco' in params['dataset']:
		attparser = cocoParser.CocoParser()
	elif 'refclef' in params['dataset']:
		attparser = clefParser.ClefParser()

	for i, sent in enumerate(sents):
		parse = sent['parse']
		try:
			attparser.reset(parse)
			sent['atts'] = attparser.decompose() # return list of atts, i.e., {r1: [man], r2: [blue], r3: [], ...}
			sent['left'] = attparser.leftWords() # return list of (wd, pos), excluding stopping words
		except:
			sent['atts'] = {'r1': ['none'], 'r2': ['none'], 'r3': ['none'], 'r4': ['none'], 'r5': ['none'],
			'r6': ['none'], 'r7': ['none'], 'r8': ['none']}
			sent['left'] = attparser.leftWords()
		if i % 100 == 0:
			print('%s/%s has been decomposed into attributes r1-r8.' % (i+1, len(sents)))

	# analyze
	analyze(sents)

	# save
	with open(osp.join('cache/parsed_atts/', dataset_splitBy, 'sents.json'), 'w') as io:
		json.dump(sents, io)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='split By')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)

