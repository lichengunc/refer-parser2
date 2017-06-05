"""
This code will convert senna's chunk 
[('Biplab', 'S-NP'), ('is', 'S-VP'), ('a', 'B-NP'), ('good', 'I-NP'), ('boy', 'E-NP'), ('.', 'O')]
into [(NP, Biplab), (VP, is), (NP, good boy), (O, .)]

We will also do cleaning on the chunked phrase, by excluding all location words like 'left', 'right', etc.
For example, (NP, right white dog) -> (NP, white dog)

We read cache/senna_sents/dataset_splitBy/sents.json and save the chucking redsults into 
cache/chunked_sents/dataset_splitBy/sents.json
"""
import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json

# nltk's stopping words
import nltk
nltk.data.path.append('/Users/liyu/Documents/nltk_data')
# nltk.data.path.append('/mnt/ilcompf6d0/user/liyu/Developments/nltk_data')
from nltk.corpus import stopwords
stop_words = stopwords.words("english") + ['.', ',', ':', '(', ')', '"', "'s", '!', 
'between', 'against', 'above', 'below', 'up', 'down', 'out', 'off', 'over']
stop_words.remove('and')  # we may need 'and' token, e.g., black and white

# location words
location_words =  ['right', 'left', 'top', 'bottom', 'middle', 'mid', 'second', '2nd', 'first', '1st', 'front', 
'closest', 'nearest', 'center', 'central', 'third', '3rd', 'corner', 'upper', 'back', 'behind', 'far', 'anywhere', 
'leftmost', 'lower', 'rightmost', 'farthest', 'furthest', 'next', 'last', 'fourth', '4th', 'up', 'above', 'below', 
'down', 'side']

def extract_chunk(senna):
	"""
	senna = {chunk, pos, srl, syntax_tree, verbs, words, ner}
	where chunk = [(the, B-NP), (lady, E-NP), ...], there are B, I, E, S, O prefix in total.
	We extract the chunk in to [(phrase, phrase_type)], e.g.,
	[('the lady', 'NP'), ('with', 'PP'), 'the blue shirt', 'NP']

	Besides, we specifically deal with such case: 
	sent = 'boy', senna's chunk = [('boy', 'O')], senna's pos = [('boy', 'NN')]
	We also consider this single word to be NP
	"""
	raw_chunk = senna['chunk']
	chunk = []
	phrase, pix = '', 0
	for c in raw_chunk:
		if pix > 0:
			phrase += ' '
		phrase += c[0]
		pix += 1
		if 'E-' in c[1] or 'S-' in c[1]:
			ptype = c[1][2:] 
			chunk += [(phrase, ptype)]
			phrase, pix = '', 0
		if c[1] == 'O':
			if len(raw_chunk) == 1: 
				if senna['pos'][0][1] == 'NN':  # when sentence = 'boy', senna ouputs 'O' but we take it as 'NP'
					chunk += [(phrase, 'NP')]
			else:
				chunk += [(phrase, 'O')]
			phrase, pix = '', 0
	return chunk

def extract_NPs(chunk):
	"""
	Given chunk [(phrase, phrase_type)], e.g., [('the lady', 'NP'), ('with', 'PP'), 'the blue shirt', 'NP'],
	we extract the NPs with stopping and location words filtered out, and return list of noun phrases.
	"""
	forbid_wds = stop_words + location_words
	NPs = []
	for phrase, ptype in chunk:
		if ptype == 'NP':
			filtered_wds = []
			for wd in phrase.split():
				if wd not in forbid_wds:
					filtered_wds += [wd]
			if len(' '.join(filtered_wds)) > 0:
				NPs += [' '.join(filtered_wds)]
	return NPs

def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/chunked_sents/'+dataset_splitBy):
		os.makedirs('cache/chunked_sents/'+dataset_splitBy)

	# load senna_sents = [{sent_id, tokens, sent, senna}]
	# where senna = {chunk, pos, srl, syntax_tree, verbs, words, ner}
	path_to_senna_sents = osp.join('cache/senna_sents', dataset_splitBy, 'sents.json')
	sents = json.load(open(path_to_senna_sents))

	# chunk convert
	for i, sent in enumerate(sents):
		senna = sent['senna']
		chunk = extract_chunk(senna)
		NPs = extract_NPs(chunk)
		sent['chunk'] = chunk
		sent['NPs'] = NPs
		if i % 1000 == 0:
			print('%s/%s done.' % (i+1, len(sents)))

	# save
	cur_folder = os.path.abspath('.')
	output_path = osp.join(cur_folder, 'cache/chunked_sents/'+dataset_splitBy, 'sents.json')
	with open(output_path, 'w') as io:
		json.dump(sents, io)	
	print('chunked_sents saved in %s.' % output_path)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='dataset name')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)