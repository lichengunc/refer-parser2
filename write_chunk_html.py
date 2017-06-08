import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json
import operator
import random
random.seed(8)

def write_structures(html, sents):
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

	html.write('<table border>')
	html.write('<tr style="font-weight:bold"><td></td>')
	html.write('<td>Top Phrase Structs</td><td>Number</td><td>Percentage</td><td>Accumulated</td><td>Example</td></tr>')
	total_num = sum(struct_to_num.values())
	acc = 0
	for j, (struct, num) in enumerate(sorted_structs[:20]):
		acc += num
		html.write('<tr><td>%02d</td>' % j)
		html.write('<td>%s</td>' % struct)
		html.write('<td>%s</td>' % num)
		html.write('<td>%.2f%%</td>' % (num*100.0/total_num))
		html.write('<td>%.2f%%</td>' % (acc*100.0/total_num))
		html.write('<td>%s</td>' % (random.choice(struct_to_examples[struct])))
		html.write('</td>')
		html.write('</tr>')
	html.write('</table>')

def write_info(html, sents):
	# NP usage in the raw chunks
	NP_usage = 0
	for sent in sents:
		chunk = sent['chunk']
		NPs = [ck for ck in chunk if ck[1] == 'NP']
		if len(NPs) > 0:
			NP_usage += 1
	html.write('<p>%.2f%% expressions have NPs' % (NP_usage*100.0/len(sents)))

	# NP usage in the filtered NPs
	cleaned_NP_usage = 0
	for sent in sents:
		if len(sent['NPs']) > 0:
			cleaned_NP_usage += 1
	html.write(', and %.2f%% cleaned NPs.</p>' % (cleaned_NP_usage*100.0/len(sents)))

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

	html.write('<p>Each expression and has %.2f NPs (%.2f cleaned NPs), %.2f PPs, %.2f ADVPs, %.2f ADJPs. </p>' % (total_NPs*1.0/len(sents), 
		total_cleaned_NPs*1.0 / len(sents), total_PPs*1.0/len(sents), total_ADVPs*1.0/len(sents), total_ADJPs*1.0/len(sents)))
	html.write('<p>Each expression has %.2f words, among which are %.2f NP words.</p>' % (total_wds/len(sents), total_NP_wds*1.0 / len(sents) ))
	html.write('<p>Each NP has %.2f words' % (total_NP_wds*1.0/total_NPs))
	html.write(', and each cleaned NP has %.2f words.</p>' % (total_cleaned_NP_wds*1.0 / total_cleaned_NPs))


def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/chunk_html/' + dataset_splitBy):
		os.makedirs('cache/chunk_html/' + dataset_splitBy)

	# load chunked sents = [{sent_id, sent, chunk, NPs, senna, tokens}]
	# where chunk is list of [(phrase, phrase_type)]
	# and NPs is list of noun phrases
	path_to_chunked_sents = osp.join('cache/chunked_sents', dataset_splitBy, 'sents.json')
	sents = json.load(open(path_to_chunked_sents))

	# write htmls
	num_per_page = params['num_per_page']
	for page_id, s in enumerate(range(0, len(sents), num_per_page)):
		html = open(osp.join('cache/chunk_html', dataset_splitBy, str(page_id)+'.html'), 'w')
		html.write('<html><body><h2>Show %s sentences and their phrase structures.' % len(sents))
		html.write('<table border>')
		html.write('<tr style="font-weight:bold"><td></td>')
		html.write('<td>sent_id</td>')
		html.write('<td><b>Referring-expression</b></td>')
		html.write('<td>Phrase Structure</td>')
		html.write('<td>Noun Phrase(s)</td>')
		html.write('<td>Noun Word(s)</td></tr>')
		for j in range(s, min(s+num_per_page, len(sents))):
			if j % 2 == 0:
				color_str = '#eef'
			else:
				color_str = '#fee'	
			# fetch info of this sent
			sent_id = sents[j]['sent_id']
			sent_txt = sents[j]['sent'].encode('ascii', 'ignore').decode('ascii')
			chunk_txt = ' '.join(['(%s, %s)' % (ck[0], ck[1]) for ck in sents[j]['chunk']])
			NPs_txt = ' '.join(['(%s, NP)' % phrase for phrase in sents[j]['NPs']])
			NNs_txt = ' '.join(['(%s, NN)' % phrase for phrase in sents[j]['NNs']])
			# write a row of the info
			html.write('<tr style="background-color:%s"><td>%06d</td>' % (color_str, j))
			html.write('<td>%s</td>' % sent_id)
			html.write('<td style="width:400px">%s</td>' % sent_txt)
			html.write('<td style="width:400px">%s</td>' % chunk_txt)
			html.write('<td style="width:400px">%s</td>' % NPs_txt)
			html.write('<td style="width:400px">%s</td>' % NNs_txt)
			html.write('</td>')
			html.write('</tr>')
		html.write('</table>')
		html.write('</body></html>')
		print('Page %s written.' % page_id)

	# write summary
	html = open(osp.join('cache/chunk_html', dataset_splitBy, 'main.html'), 'w')
	html.write('<html><head><style>.sm{color:#009;font-size:0.8em}</style></head>')
	html.write('<body>')

	# write phrase structures
	write_structures(html, sents)

	# write other info
	write_info(html, sents)

	# write pages
	html.write('<ul>')
	for page_id, s in enumerate(range(0, len(sents), num_per_page)):
		page_html = str(page_id)+'.html'
		print(page_html)
		html.write('<li><a target="_blank" href="%s"> page_id%s</a></li>' % (page_html, page_id))
	html.write('</ul>')


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