__author__ = 'licheng'

"""
r1: [lemma of head word]
r2: [color word describing r1]
r3: [size word describing r1]
r4: [location word describing r1], e.g., upper dog, dog on the left (of the picture)
r5: [relative location and object], e.g., person under the door, dog on the table, dog on the left of the cat,
    Note, we also take "second cat from left", i.e., [r5 = second_left, r6 = self]
r6: [generic attribute describing r1], i.e., other JJ and dep attributes describing head word
"""

from baseParser import BaseParser

class CocoParser(BaseParser):

    def __init__(self):
        BaseParser.__init__(self, 'refcoco')

    def reset(self, parse):
        BaseParser.reset(self, parse)
        # Now, let's extract dependencies related to ordinary words
        self.Deps['ord'] = [dep for dep in self._dependencies if dep[1] == self.r1[0] and dep[3] in
                            self.config.ordinal_table['words']] if self.r1[0]!='none' else []
        self.rels['ord_prep'] = [dep for dep in self.rels['prep'] if dep[1] in self.config.ordinal_table['words']]

    def decompose(self):
        # r2: color
        color_wds  = [dep[3] for dep in self.Deps['att'] if dep[3] in self.config.color_table['wordtoix']]
        color_wds += [dep[3] for dep in self.Deps['prep_in'] if dep[3] in self.config.color_table['wordtoix']]
        for wd in color_wds:
            ix = self.config.color_table['wordtoix'][wd]
            self.r2 += [self.config.color_table['ixtoword'][ix]]

        # r3: size
        size_wds = [dep[3] for dep in self.Deps['att'] if dep[3] in self.config.size_table['words']]
        for wd in size_wds:
            ix = self.config.size_table['wordtoix'][wd]
            self.r3 += [self.config.size_table['ixtoword'][ix]]

        # r4: absolute location (no ordinal word)
        location_wds = []
        if len(self.Deps['ord']) + len(self.rels['ord_prep']) == 0:
            # 1) left sth.
            location_wds =  [dep[3] for dep in self.Deps['att'] if dep[3] in self.config.location_table['words']]
            # 2) sth in/on the left.
            commonDeps = self.Deps['prep_on']+self.Deps['prep_in']+self.Deps['prep_at']
            position_deps =  [dep for dep in commonDeps if dep[3] in self.config.position_table['words']]
            if len(self.Deps['prep_of']) == 0:
                location_wds += [dep[3] for dep in position_deps]
            else:
            # 3) sth in/on/at the left of the image.
            # 4) sth of sth in/on/at the left.
                ForbiddenWds = ['image', 'picture', 'im', 'pic']
                position_id  = min([dep[4] for dep in position_deps]) if len(position_deps) > 0 else 0
                position_of_objects = [dep[3] for dep in self.Deps['prep_of'] if dep[3] not in ForbiddenWds and dep[4] > position_id]
                if len(position_of_objects) == 0:
                    location_wds += [dep[3] for dep in position_deps]
         # add to r4
        for wd in location_wds:
            ix = self.config.location_table['wordtoix'][wd]
            self.r4 += [self.config.location_table['ixtoword'][ix]]

        # r5, r6: relative location and object
        '''
        e.g., case 1 and 2:
              sent         = 'players at the door.'  or 'players from the river.'
              dependencies = [('root', 'ROOT', '0', 'players', '1'),
                              ('det', 'door', '4', 'the', '3'),
                              ('prep_at', 'players', '1', 'door', '4')]
              case 3:
              sent         = 'players on the left of the dog.'
              dependencies = [('root', 'ROOT', '0', 'players', '1'),
                              ('det', 'left', '4', 'the', '3'),
                              ('prep_on', 'players', '1', 'left', '4'),
                              ('det', 'dog', '7', 'the', '6'),
                              ('prep_of', 'players', '1', 'dog', '7')]

              case 4:
              sent         = 'second left man.'
              dependencies = [('root', 'ROOT', '0', 'man', '3'),
                              ('amod', 'man', '3', 'second', '1'),
                              ('amod', 'man', '3', 'left', '2')]
              case 5:
              sent         = 'second man from left.'
              dependencies = [('root', 'ROOT', '0', 'left', '4'),
                              ('amod', 'man', '2', 'second', '1'),
                              ('nsubj', 'left', '4', 'man', '2'),
                              ('prep', 'man', '2', 'from', '3')]
              case 6:
              sent         = 'man second from right.'
              dependencies = [('root', 'ROOT', '0', 'second', '2'),
                              ('nn', 'second', '2', 'man', '1'),
                              ('prep_from', 'second', '2', 'right', '4')]
              case 7:
              sent         = 'second from right man.'
              dependencies = [('root', 'ROOT', '0', 'second', '1'),
                              ('amod', 'man', '4', 'right', '3'),
                              ('prep_from', 'second', '1', 'man', '4')]
        Note, in vicente's matlab, the parsing differs at adding punct in the end.
        '''
        if len(self.Deps['ord']) + len(self.rels['ord_prep']) == 0:
            # 1) the dog from the river
            ForbiddenWds = self.config.position_table['words']+self.config.color_table['words']
            rel_pairs = [(dep[0], dep[3]) for dep in self.Deps['prep'] if dep[0] in self.config.relative_preps_table['words']
                         if dep[3] not in ForbiddenWds]
            for pair in rel_pairs:
                self.r5 += [pair[0]]
                self.r6 += [pair[1]]
            # 2) the dog on/in/at the table
            commonDeps = self.Deps['prep_on']+self.Deps['prep_in']+self.Deps['prep_at']
            ForbiddenWds = self.config.position_table['words']+self.config.color_table['words']
            rel_pairs = [(dep[0], dep[3]) for dep in commonDeps if dep[3] not in ForbiddenWds]
            for pair in rel_pairs:
                self.r5 += [pair[0]]
                self.r6 += [pair[1]]
            # 3) the dog on/in/at/to the left of table.
            # 4) the face of woman on the left of the window. Note we only detect position_of_objects
            commonDeps = self.Deps['prep_on']+self.Deps['prep_in']+self.Deps['prep_at']+self.Deps['prep_to']
            ForbiddenWds = ['image', 'picture', 'im', 'pic']
            position_deps = [dep for dep in commonDeps if dep[3] in self.config.position_table['words']]
            position_id = min([dep[4] for dep in position_deps]) if len(position_deps) > 0 else 0 # find the earliest position for 'left', 'right', 'top', ...
            position_of_objects = [dep[3] for dep in self.Deps['prep_of'] if dep[3] not in ForbiddenWds and dep[4] > position_id]  # 'of' must appear after position_id
            for dep in position_deps:
                if len(position_of_objects) > 0:
                    for of_object in position_of_objects:
                        self.r5 += [dep[0]+'_'+dep[3]]
                        self.r6 += [of_object]
        else:
            position_wds, ordinary_wds = [], []
            if len(self.Deps['ord']) > 0:
                ordinary_wds = [dep[3] for dep in self.Deps['ord']]
                # 4) second left man
                position_wds = [dep[3] for dep in self.Deps['att'] if dep[3] in self.config.position_table['words']]
                # 5) second man from left
                position_wds += [dep[3] for dep in self._dependencies if dep[3] in self.config.position_table['words']]  # no pattern, so search from all dependencies
            if len(self.rels['ord_prep']) > 0:
                ordinary_wds = [dep[1] for dep in self.rels['ord_prep']]
                # 6) man second from right
                position_wds = [dep[3] for dep in self.rels['ord_prep'] if dep[3] in self.config.position_table['words']]
                # 7) second from right man
                position_wds += [dep[3] for dep in self.Deps['att'] if dep[3] in self.config.position_table['words']]
            # add to r5 and r6
            if len(position_wds) > 0:
                self.r5 += [ordinary_wds[0]+'_'+position_wds[0]]
                self.r6 += ['self']

        # r7: generic attribute
        ForbiddenWds = self.config.size_table['words'] + self.config.color_table['words'] + self.config.position_table['words'] \
                       + self.config.location_table['words'] + self.config.ordinal_table['words']
        generic_wds = [dep[3] for dep in self.Deps['att'] if dep[3] not in ForbiddenWds]
        for gwd in generic_wds:
            gpos = [wd[1]['PartOfSpeech'] for wd in self._words if wd[0] == gwd][0]
            if gpos[:2] == 'JJ':
                self.r7 += [gwd]

        self.r2 = ['none'] if len(self.r2) == 0 else self.r2
        self.r3 = ['none'] if len(self.r3) == 0 else self.r3
        self.r4 = ['none'] if len(self.r4) == 0 else self.r4
        self.r5 = ['none'] if len(self.r5) == 0 else self.r5
        self.r6 = ['none'] if len(self.r6) == 0 else self.r6
        self.r7 = ['none'] if len(self.r7) == 0 else self.r7

        # left words -> r8
        left_wds = [word[0] for word in self.leftWords()]
        self.r8 = ['none'] if len(left_wds) == 0 else left_wds

        return {'r1': self.r1, 'r2': self.r2, 'r3': self.r3, 'r4': self.r4, 'r5': self.r5, 'r6': self.r6, 'r7': self.r7, 'r8': self.r8}

if __name__ == '__main__':
    import sys
    from pprint import pprint
    import os.path as osp
    ROOT_DIR = osp.abspath('/playpen/licheng/Documents/referit')
    sys.path.insert(0, osp.join(ROOT_DIR, 'lib', 'utils'))
    from corenlp.corenlp import StanfordCoreNLP
    parser_path = osp.join(ROOT_DIR, 'lib', 'utils', 'corenlp', 'stanford-corenlp-full-2015-01-30')
    stanfordParser = StanfordCoreNLP(parser_path)

    sent = 'a bunch of flower at the door.'
    parse = stanfordParser.raw_parse(sent)['sentences'][0]
    pprint(parse['dependencies'])

    attParser = CocoParser()
    attParser.reset(parse)
    pprint(attParser.decompose())
    pprint(attParser.leftWords())





















