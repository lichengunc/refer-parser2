import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json
import operator
import random

def analyze_structure(sents):
	"""
	The input sents = [{sent_id, sent, chunk, NPs, senna, tokens}]
	where chunk is list of [(phrase, phrase_type)], and NPs is list of noun phrases
	We analyze phrase structure
	"""
	struct_to_num = {}
	struct_to_examples = {}
	for sent in sents:
		chunk = sent['chunk']
		struct = ' '.join([ck[1] for ck in chunk])
		struct_to_num[struct] = struct_to_num.get(struct, 0) + 1
		if struct not in struct_to_examples:
			struct_to_examples[struct] = []
		struct_to_examples[struct] += [sent['sent']]
	sorted_structs = sorted(struct_to_num.items(), key=operator.itemgetter(1))
	sorted_structs.reverse()

	print('%25s: %10s  %6s  %8s' % ('structure', 'number', 'perc.', 'acc.'))
	total_num = sum(struct_to_num.values())
	acc = 0
	for struct, num in sorted_structs[:20]:
		acc += num
		print('%25s: %10d  %6.3f%%  %4.3f%%, e.g., %s' % (struct, num, num*100.0/total_num, acc*100.0/total_num, random.choice(struct_to_examples[struct])))

def analyze_NP(sents):
	# NP usage in the raw chunks
	NP_usage = 0
	for sent in sents:
		chunk = sent['chunk']
		NPs = [ck for ck in chunk if ck[1] == 'NP']
		if len(NPs) > 0:
			NP_usage += 1
	print('%.2f%% (%s/%s) expressions have NPs.' % (NP_usage*100.0/len(sents), NP_usage, len(sents)))

	# NP usage in the filtered NPs
	cleaned_NP_usage = 0
	for sent in sents:
		if len(sent['NPs']) > 0:
			cleaned_NP_usage += 1
	print('%.2f%% (%s/%s) expressions have cleaned NPs.' % (cleaned_NP_usage*100.0/len(sents), cleaned_NP_usage, len(sents)))

	# average #NP in each expression
	total_NPs, total_cleaned_NPs, total_PPs, total_VPs, total_ADVPs, total_ADJPs = 0, 0, 0, 0, 0, 0
	total_wds = 0
	total_NP_wds = 0
	total_cleaned_NP_wds = 0
	for sent in sents:
		for ck in sent['chunk']:
			if ck[1] == 'NP':
				total_NPs += 1
				total_NP_wds += len(ck[0].split())
			if ck[1] == 'PP':
				total_PPs += 1
			if ck[1] == 'ADVP':
				total_ADVPs += 1
			if ck[1] == 'ADJP':
				total_ADJPs += 1
		total_wds += len(sent['tokens'])
		# check cleaned NPs
		total_cleaned_NPs += len(sent['NPs'])
		total_cleaned_NP_wds += sum([len(phrase.split()) for phrase in sent['NPs']])

	print('Each expression and has %.2f NPs (%.2f cleaned NPs), %.2f PPs, %.2f ADVPs, %.2f ADJPs,' % (total_NPs*1.0/len(sents), 
		total_cleaned_NPs*1.0 / len(sents), total_PPs*1.0/len(sents), total_ADVPs*1.0/len(sents), total_ADJPs*1.0/len(sents)))
	print('Each expression has %.2f words, among which are %.2f NP words.' % (total_wds/len(sents), total_NP_wds*1.0 / len(sents) ))
	print('Each NP has %.2f words.' % (total_NP_wds*1.0/total_NPs))
	print('Each cleaned NP has %.2f words.' % (total_cleaned_NP_wds*1.0 / total_cleaned_NPs))


def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/chunk_html/' + dataset_splitBy):
		os.makedirs('cache/chunk_html/' + dataset_splitBy)

	# load chunked sents = [{sent_id, sent, chunk, NPs, senna, tokens}]
	# where chunk is list of [(phrase, phrase_type)]
	# and NPs is list of noun phrases
	path_to_chunked_sents = osp.join('cache/chunked_sents', dataset_splitBy, 'sents.json')
	sents = json.load(open(path_to_chunked_sents))

	# analyze phrase structure
	analyze_structure(sents)

	# analyze the usage of NPs
	analyze_NP(sents)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='split By')
	parser.add_argument('--num_per_page', type=int, default=10000, help='number of pages to be written')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)