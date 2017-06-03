"""
This code chunk sentences into NP, VP, PP, O, etc.
It uses the SENNA tool, (https://github.com/biplab-iitb/practNLPTools, https://pypi.python.org/pypi/practnlptools/1.0), 
to perform the chunking.

The results will be saved in cache/chunked_sents/dataset_splitBy/sents.json
The sents.json = [{sent_id, sent, senna}], where senna = {chunk, pos, srl, syntax_tree, verbs, words, ner}
"""
import sys
import os
import os.path as osp
from pprint import pprint
from Queue import Queue
from threading import Thread, Lock
import time
import argparse
import json
# import SENNA tool
from practnlptools.tools import Annotator

def senna_sents(sents, params):
	"""
	The input sents is list of [{sent_id, sent, raw, tokens}]
	Return sents of [{sent_id, sent, raw, tokens, chunk}]
	"""
	num_sents = len(sents)

	# enqueue
	q = Queue()
	for i in range(num_sents):
		q.put((i, sents[i]))

	# work: dequeue and do job
	def worker():
		annotator = Annotator()
		while True:
			i, sent = q.get()
			try:
				senna = annotator.getAnnotations(sent['sent'])
			except:
				senna = annotator.getAnnotations('none')
			if i % 100 == 0:
				print('%s/%s done.' % (i, num_sents))
			sents[i]['senna'] = senna  
			sents[i]['senna'].pop('dep_parse', None) # including chunk, pos, srl, syntax_tree, verbs, words, ner
			q.task_done()

	# workers
	for w in range(params['num_workers']):
		t = Thread(target=worker)
		t.daemon = True
		t.start()
	q.join()


def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/senna_sents/' + dataset_splitBy):
		os.makedirs('cache/senna_sents/' + dataset_splitBy)

	# load refer
	sys.path.insert(0, 'pyutils/refer')
	from refer import REFER
	refer = REFER(params['data_root'], params['dataset'], params['splitBy'])
	
	# parse sents	
	sents = refer.Sents.values()
	senna_sents(sents, params)

	# pop unnecessary keys 
	for sent in sents:
		sent.pop('raw', None)

	# save
	with open(osp.join('cache/senna_sents/'+dataset_splitBy, 'sents.json'), 'w') as io:
		json.dump(sents, io)


if __name__ == '__main__':

	# input
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_root', default='data', help='dataset root directory')
	parser.add_argument('--dataset', default='refcoco', help='dataset name')
	parser.add_argument('--splitBy', default='unc', help='split By')
	parser.add_argument('--num_workers', type=int, default=2, help='number of workers')
	args = parser.parse_args()
	params = vars(args)

	# main
	main(params)