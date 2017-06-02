__author__ = 'licheng'

from attparser.clefParser import ClefParser
from attparser.cocoParser import CocoParser
import cPickle as pickle
import sys
import argparse
import os.path as osp
ROOT_DIR = osp.abspath(osp.join(osp.dirname(__file__), '..', '..'))

def getAttributes(dataset):

    # load parses
    sentToParse = pickle.load(open(osp.join(ROOT_DIR, 'cache', dataset, 'sentToParse.p')))

    # load configuration and AttributeParser
    if dataset == 'refclef':
        parser = ClefParser()
    elif dataset in ['refcoco', 'refcoco+', 'refcoco++']:
        parser = CocoParser()
    else:
        print 'No parser prepared for this dataset.'
        sys.exit()

    # attribute parsing
    sentToAtts = {}
    sentToLefts = {}
    i = 0
    for sent_id, parse in sentToParse.items():
        try:
            parser.reset(parse)
            sentToAtts[sent_id] = parser.decompose()  # return list of atts, i.e., {'r1': [atts], 'r2': [atts], ...}
            sentToLefts[sent_id] = parser.leftWords() # return list of (wd, pos)
        except:
            sentToAtts[sent_id] = {'r1': ['none'], 'r2': ['none'], 'r3': ['none'], 'r4': ['none'], 'r5': ['none'],
                                   'r6': ['none'], 'r7': ['none'], 'r8': ['none']}
            sentToLefts[sent_id] = parser.leftWords()
        print '%s out of %s done [sent_id=%s, sent: %s].' % (i+1, len(sentToParse), sent_id, parse['text'])
        i += 1

    # save attToAtts
    file_name = osp.join(ROOT_DIR, 'cache', dataset, 'sentToAtts.p')
    with open(file_name, 'w') as outfile:
        pickle.dump(sentToAtts, outfile)

    # save attToLefts
    file_name = osp.join(ROOT_DIR, 'cache', dataset, 'sentToLefts.p')
    with open(file_name, 'w') as outfile:
        pickle.dump(sentToLefts, outfile)

    # analyse
    analyze(sentToAtts)

    # view
    writeHTML(dataset, sentToParse, sentToAtts, sentToLefts)

def analyze(sentToAtts):
    # do some statistics
    usage = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0, 'r7': 0, 'r8': 0}
    for sent_id, atts in sentToAtts.items():
        for r in usage:
            usage[r] = usage[r]+1 if atts[r] != ['none'] else usage[r]
    for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8']:
        usage[r] /= float(len(sentToAtts))
        print 'Usage of %s is %.2f%%' % (r, usage[r]*100)

def writeHTML(dataset, sentToParse, sentToAtts, sentToLefts):
    file_name = 'sentToAtts.html'
    html = open(osp.join(ROOT_DIR, 'results', dataset, file_name), 'w')
    html.write('<html><body><h2>Show %s sentences and their attribute parses.' % len(sentToAtts))
    html.write('<table border>')
    html.write('<tr style="font-weight:bold"><td></td><td></td>')
    html.write('<td><b>Referring-expression</b></td>')
    html.write('<td>Entry-level name</td><td>Color</td>')
    html.write('<td>Size</td><td>Abs. Location</td>')
    html.write('<td>Rel. Location</td><td>Rel. Object</td><td>Other</td><td>Left Words</td></tr>')
    i = 0
    for sent_id, parse in sentToParse.items():
        if i%2 == 0:
            color_str = '#eef'
        else:
            color_str = '#fee'
        sent = parse['text']
        atts = sentToAtts[sent_id]
        lefts = sentToLefts[sent_id]

        html.write('<tr style="background-color:%s"><td>%05d</td>' % (color_str, i))
        html.write('<td>%s</td>' % sent_id)
        html.write('<td style="width:400px">%s</td>' % sent)
        for r in ['r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']:
            atts[r] = atts[r][0] if atts[r][0] != 'none' else ''
            html.write('<td style="width:100px">%s</td>' % atts[r])
        html.write('<td style="width:400px">')
        for left in lefts:
            html.write('%s [%s],&nbsp' % (left[0], left[1]))
        html.write('</td>')
        html.write('</tr>')
        i += 1
    html.write('</table>')
    html.write('</body></html>')
    print 'Web page written.'

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate expressions on testing split.")
    parser.add_argument(dest='dataset', type=str, help='dataset name')
    args = parser.parse_args()
    params = vars(args)

    getAttributes(params['dataset'])





