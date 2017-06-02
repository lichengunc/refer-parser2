__author__ = 'licheng'

"""
BaseParser defines:
reset: initialize parse, head word, rels and Deps.
"""

from nltk.tree import *
import sys
from nltk.corpus import stopwords
import os.path as osp
import config
import head

class BaseParser():
    def __init__(self, dataset):
        if dataset == 'refclef':
            self.config = config.configCLEF()
            self._headMode = 'vicente'
        elif dataset == 'refcoco' or dataset == 'refcoco+':
            self.config = config.configCOCO()
            self._headMode = 'licheng'
        else:
            print 'No configuration set yet.'
            sys.exit()

    def reset(self, parse):
        # load parse
        self._tree = Tree.fromstring(parse['parsetree'])
        self._dependencies = parse['dependencies']
        self._words = parse['words']
        self._text  = parse['text']

        # reset seven attributes
        self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.r7 = [], [], [], [], [], [], []

        # find head word
        self.head_word, _ = head.findHead(self._tree, mode = self._headMode)
        if self.head_word != '' and self.head_word != None:
            self.r1 = [wd[1]['Lemma'] for wd in self._words if wd[0] == self.head_word]
            self.r1 = [self.r1[0]]  # we only need one
        else:
            self.r1 = ['none']

        # dependency's relations that have 'prep'
        rels_prep      = [dep for dep in self._dependencies if 'prep' in dep[0]]
        rels_prep_in   = [dep for dep in self._dependencies if 'prep_in' in dep[0]]
        rels_prep_on   = [dep for dep in self._dependencies if 'prep_on' in dep[0]]
        rels_prep_at   = [dep for dep in self._dependencies if 'prep_at' in dep[0]]
        rels_prep_to   = [dep for dep in self._dependencies if 'prep_to' in dep[0]]
        rels_prep_from = [dep for dep in self._dependencies if 'prep_from' in dep[0] or 'prepc_from' in dep[0]]
        rels_prep_of   = [dep for dep in self._dependencies if 'prep_of' in dep[0]]
        rels_det       = [dep for dep in self._dependencies if 'det' in dep[0]]

        # dependency's sources equal to head_word
        rels_direct    = [dep for dep in self._dependencies if dep[1] == self.head_word] if self.r1[0]!='none' else []
        direct_att_dep = [dep for dep in rels_direct if dep not in rels_prep + rels_det]
        prep_dep       = [dep for dep in rels_direct if dep in rels_prep]
        prep_in_dep    = [dep for dep in rels_direct if dep in rels_prep_in]
        prep_on_dep    = [dep for dep in rels_direct if dep in rels_prep_on]
        prep_of_dep    = [dep for dep in rels_direct if dep in rels_prep_of]
        prep_from_dep  = [dep for dep in rels_direct if dep in rels_prep_from]
        prep_at_dep    = [dep for dep in rels_direct if dep in rels_prep_at]
        prep_to_dep    = [dep for dep in rels_direct if dep in rels_prep_to]

        # initialize types of dependencies
        self.rels = {}
        self.rels['prep']      = rels_prep
        self.rels['prep_in']   = rels_prep_in
        self.rels['prep_on']   = rels_prep_on
        self.rels['prep_at']   = rels_prep_at
        self.rels['prep_to']   = rels_prep_to
        self.rels['prep_from'] = rels_prep_from
        self.rels['prep_of']   = rels_prep_of

        # initialize types of dependencies whose source is head word
        # Deps denots Direct dependencies
        self.Deps = {}
        self.Deps['att']       = direct_att_dep
        self.Deps['prep']      = prep_dep
        self.Deps['prep_in']   = prep_in_dep
        self.Deps['prep_on']   = prep_on_dep
        self.Deps['prep_of']   = prep_of_dep
        self.Deps['prep_from'] = prep_from_dep
        self.Deps['prep_at']   = prep_at_dep
        self.Deps['prep_to']   = prep_to_dep

    def leftWords(self):
        all_wds = [word[0] for word in self._words]
        att_wds = [self.head_word] + self.r2 + self.r3 + self.r4 + self.r7
        # we then add r5, r6 to att_wds, need some tricks
        for wd in self.r5:
            if 'prep' in wd:
                wd = wd[5:] # prep_on_left -> on_left
                idx = wd.find('_')
                if idx >= 0:
                    att_wds += [wd[:idx], wd[idx+1:]]
                else:
                    att_wds += [wd] # prep_from -> from
            else: # ordinary_position, e.g., second_left
                idx = wd.find('_')
                att_wds += [wd[:idx], wd[idx+1:]]
        for wd in self.r6:
            att_wds = att_wds + [wd] if wd != 'self' else att_wds
        # the left word set
        left_wds = list(set(all_wds).difference(set(att_wds)))
        # word to POS dictionary
        wdToPOSs = {word[0]: [] for word in self._words}
        for word in self._words:
            wdToPOSs[word[0]] += [word[1]]
        # return left words
        # stopwds = ['the', 'of', 'a', 'an', ',', '.', 'on', 'in', 'from', 'at', 'of', 'to', 'and', 'or', '(', ')', 'that', 'this', 'it']
        stopwds = stopwords.words("english") + ['.', ',', ':', '(', ')', '"', "'s", '!', 'between', 'against', 'above',
                                                'below', 'up', 'down', 'out', 'off', 'over']
        left_words = [(wd, wdToPOSs[wd][0]['PartOfSpeech']) for wd in left_wds if wd not in stopwds]
        return left_words

if __name__ == '__main__':
    from pprint import pprint

    ROOT_DIR = osp.abspath('/playpen/licheng/Documents/referit')
    sys.path.insert(0, osp.join(ROOT_DIR, 'lib', 'utils'))
    from corenlp.corenlp import StanfordCoreNLP
    parser_path = osp.join(ROOT_DIR, 'lib', 'utils', 'corenlp', 'stanford-corenlp-full-2015-01-30')
    stanfordParser = StanfordCoreNLP(parser_path)

    sent = 'players close to us in dark uniform'
    parse = stanfordParser.raw_parse(sent)['sentences'][0]
    pprint(parse)

    attParser = BaseParser('refclef')
    attParser.reset(parse)


