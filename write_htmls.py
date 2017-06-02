import sys
import os
import os.path as osp
from pprint import pprint
import time
import argparse
import json

attribute_names = {'r1': 'entry-level name', 'r2': 'color', 'r3': 'size', 'r4': 'abs. location', 
'r5': 'rel. location', 'r6': 'rel. object', 'r7': 'other atts.', 'r8': 'left words'}

def analyze(sents):
	# do some statistics
	usage = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0}
	for sent in sents:
		for r in usage:
			usage[r] = usage[r] + 1 if sent['atts'][r] != ['none'] else usage[r]
	for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']:
		usage[r] /= float(len(sents))
		print('Usage of %s is %.2f%%.' % (r, usage[r] * 100))
	return usage

def main(params):

	dataset_splitBy = params['dataset'] + '_' + params['splitBy']
	if not osp.isdir('cache/atts_html/' + dataset_splitBy):
		os.makedirs('cache/atts_html/' + dataset_splitBy)

	# load parsed sents with attributes, where sents.json = 
	# [{sent_id, sent, parse, atts, left, raw, tokens}]
	# where parse = {dependencies, parsetree, text, workds}, atts = {r1, r2, ...}, left = [(wd, POS)]
	path_to_parsed_atts = osp.join('cache/parsed_atts', dataset_splitBy, 'sents.json')
	sents = json.load(open(path_to_parsed_atts))

	# analyze
	usage = analyze(sents)

	# write htmls
	num_per_page = params['num_per_page']
	for page_id, s in enumerate(range(0, len(sents), num_per_page)):
		html = open(osp.join('cache/atts_html', dataset_splitBy, str(page_id)+'.html'), 'w')
		html.write('<html><body><h2>Show %s sentences and their attribute parses.' % len(sents))
		html.write('<table border>')
		html.write('<tr style="font-weight:bold"><td></td>')
		html.write('<td>sent_id</td>')
		html.write('<td><b>Referring-expression</b></td>')
		html.write('<td>Entry-level name</td><td>Color</td>')
		html.write('<td>Size</td><td>Abs. Location</td>')
		html.write('<td>Rel. Location</td><td>Rel. Object</td><td>Other</td><td>Left Words</td></tr>')
		for j in range(s, min(s+num_per_page, len(sents))):
			if j % 2 == 0:
				color_str = '#eef'
			else:
				color_str = '#fee'	
			# fetch info of this sent	
			sent_id = sents[j]['sent_id']
			sent_txt = sents[j]['sent'].encode('ascii', 'ignore').decode('ascii')
			atts = sents[j]['atts']
			left = sents[j]['left']
			# write a row of the info
			html.write('<tr style="background-color:%s"><td>%06d</td>' % (color_str, j))
			html.write('<td>%s</td>' % sent_id)
			html.write('<td style="width:400px">%s</td>' % sent_txt)
			for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']:
				att = atts[r][0] if atts[r][0] != 'none' else ''
				html.write('<td style="width:100px">%s</td>' % att)
			html.write('<td style="width:400px">')
			for l in left:
				html.write('%s [%s],&nbsp' % (l[0], l[1]))
			html.write('</td>')
			html.write('</tr>')
		html.write('</table>')
		html.write('</body></html>')
		print('Page %s written.' % page_id)

	# write summary
	html = open(osp.join('cache/atts_html', dataset_splitBy, 'main.html'), 'w')
	html.write('<html><head><style>.sm{color:#009;font-size:0.8em}</style></head>')
	html.write('<body><table border>')
	for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']:
		html.write('<h2>usage of %s [%s] is %.2f%%</h2>' % (r, attribute_names[r], usage[r]*100))
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
