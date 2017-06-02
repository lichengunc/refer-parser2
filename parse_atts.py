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
nltk.data.path.append('/Users/liyu/Documents/nltk_data')

def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/parsed_atts/' + dataset_splitBy):
		os.makedirs('cache/parsed_sents/' + dataset_splitBy)

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
		attparser.reset(parse)
		R = attparser.decompose()
		sent['atts'] = R  # {r1: [man], r2: [blue], r3: [], ...}
		if i % 100 == 0:
			print('%s/%s has been decomposed into attributes r1-r8.' % (i+1, len(sents)))
	
	# save	
	with open(osp.join('cache/parsed_atts/', dataset_splitBy, 'sents.json'), 'w') as io:
		json.dump(sents, io)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_root', default='data', help='dataset root directory')
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='split By')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)

