import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json
from utils import CocoParser


def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	path_to_parsed_sents = osp.join('cache/parsed_sents', dataset_splitBy, 'sents.json')
	parsed_sents = json.load(open(path_to_parsed_sents))

	attparser = CocoParser()
	parse = parsed_sents[0]['parse']
	attparser.reset(parse)
	pprint(attparser.decompose())
	pprint(attparser.leftWords())


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

