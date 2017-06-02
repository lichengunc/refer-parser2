"""
This code parse sentences into dependencies, parsetree, text and workds using Stanford-CoreNLP-Parser,
but current corenlp is only able to load v3.5.1 and v3.5.2.

The parsed sentences are saved in cache/parsed_sents/dataset_splitBy/sents.json
The sents.json = [{sent_id, sent, parse, raw, tokens}], where parse = {dependencies, parsetree, text, workds}
"""
import sys
import os
import os.path as osp
from pprint import pprint
from nltk.tree import *
from Queue import Queue
from threading import Thread, Lock
import time
import argparse
import json
from pyutils.corenlp import StanfordCoreNLP

def load_corenlp(params):
	# load corenlp
	b = time.time()
	core = StanfordCoreNLP(params['corenlp_model'])
	print('corenlp model loaded in %.2f seconds.' % (time.time() - b))
	return core

def parse_sents(sents, params):
	"""
	The input sents is list of [{sent_id, sent, raw, tokens}]
	The parse results if {dependencies: [(det, dog, the), (root, ROOT, dog)...]
						  parsetree: u'(ROOT (NP (NP (DT the) (JJ left) (NN dog)) (PP (IN on) (NP (DT the) (NN tree)))))'
						  text: u'the left dog on the tree'
						  words: [(u'the',
                       			  {u'CharacterOffsetBegin': u'0',
                        	 	   u'CharacterOffsetEnd': u'3',
                        	 	   u'Lemma': u'the',
                       		 	   u'NamedEntityTag': u'O',
                         	 	   u'PartOfSpeech': u'DT'}), ...]}
	Return sents = [{sent_id, sent, parse, raw, tokens}]	
	"""
	num_sents = len(sents)

	# enqueue
	q = Queue()
	for i in range(num_sents):
		q.put((i, sents[i]))

	# work: dequeue and do job
	def worker():
		core = load_corenlp(params)
		while True:
			i, sent = q.get()
			try:
				output = core.raw_parse(sent['sent'])['sentences'][0]
			except:
				output = core.raw_parse('none')['sentences'][0]
			if i % 100 == 0:
				print('%s/%s done.' % (i, num_sents))
			sents[i]['parse'] = output
			q.task_done()

	# workers
	for w in range(params['num_workers']):
		t = Thread(target=worker)
		t.daemon = True
		t.start()
	q.join()


def main(params):
	
	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/parsed_sents/'+dataset_splitBy):
		os.makedirs('cache/parsed_sents/'+dataset_splitBy)

	# load refer
	sys.path.insert(0, 'pyutils/refer')
	from refer import REFER
	refer = REFER(params['data_root'], params['dataset'], params['splitBy'])

	# parse sents
	sents = refer.Sents.values()
	parse_sents(sents, params)

	# save
	with open(osp.join('cache/parsed_sents/'+dataset_splitBy, 'sents.json'), 'w') as io:
		json.dump(sents, io)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_root', default='data', help='dataset root directory')
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='split By')
	parser.add_argument('--corenlp_model', default='models/stanford-corenlp-full-2015-01-29')
	parser.add_argument('--num_workers', type=int, default=2, help='number of workers')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)


