__author__ = 'licheng'

from nltk.tree import *

ing_allowed = ['duckling', 'frosting', 'something', 'anything', 'thing', 'king', 'nothing',
               'ring', 'wing', 'darling', 'building', 'painting', 'everything', 'string', 
               'ceiling', 'pudding',  ]
not_allowed = ['first', 'second', 'third', 'fourth', 'front', 'fifth', 'right', 'left']

def findFirstbreadthFirst(T, label):
    # input: tree, and label ('NN' or 'NP')
    # return: tree, or None
    myqueue = []
    label_len = len(label)
    for i in range(len(T)):
        myqueue.append(str(T[i])) # push the sons
    while len(myqueue) > 0:
        cur_T = Tree.fromstring( myqueue.pop(0) )  # pop the front node as current tree
        cur_label = cur_T.label()
        if len(cur_label)>=label_len and cur_label[:label_len] == label:
            if cur_T[0] in not_allowed: # in case parser take 'first', 'second' as noun
                continue
            if cur_T[0][-3:] == 'ing' and cur_T[0] not in ing_allowed: # in case parser take both 'man' and 'standing' as Noun for 'man standing under the tree'
                continue
            return cur_T
        else:
            if not isinstance(cur_T[0], str):  # if not the leaf node, i.e., 'dog', 'tree'
                for i in range(len(cur_T)):
                    myqueue.append(str(cur_T[i]))
    return None

def findLastbreadthFirst(T, label):
    myqueue = []
    label_len = len(label)
    for i in reversed(range(len(T))):
        myqueue.append(str(T[i])) # push the sons
    while len(myqueue) > 0:
        cur_T = Tree.fromstring( myqueue.pop(0) )  # pop the front node as current tree
        cur_label = cur_T.label()
        if len(cur_label)>=label_len and cur_label[:label_len] == label:
            if cur_T[0] in not_allowed:
                # in case parser take 'first', 'second' as noun
                continue
            if cur_T[0][-3:] == 'ing' and cur_T[0] not in ing_allowed: # in case parser take 'standing' as Noun for 'man standing under the tree'
                continue
            return cur_T
        else:
            if not isinstance(cur_T[0], str):  # if not the leaf node, i.e., 'dog', 'tree'
                for i in reversed(range(len(cur_T))):  # push_back from the last to the first
                    myqueue.append(str(cur_T[i]))
    return None

def findHead(T, mode='vicente'):
    if mode == 'vicente':  # find the left-most NP, and then its left-most NN
        if not T[0].label() == 'NP':
            foundNP = findFirstbreadthFirst(T[0], 'NP')
            if foundNP:
                head = findFirstbreadthFirst(foundNP, 'NN')
            else:
                head = findFirstbreadthFirst(T[0], 'NN')
        else:
            head = findFirstbreadthFirst(T[0], 'NN')
        if head == None:
            return None, -1
        else:
            head = head[0]
            idx  = [pos[0] for pos in T.pos()].index(head)
            return head, idx
    elif mode == 'licheng': # find bottom-left NP first, then search its rightmost NN son
        np_exist = T
        np_found = findFirstbreadthFirst(np_exist, 'NP')
        while np_found:
            np_exist = np_found
            np_found = findFirstbreadthFirst(np_exist, 'NP')
        if np_exist != T:
            head_tr = findLastbreadthFirst(np_exist, 'NN')
            if not head_tr: # if this NP tree has no NN son, we just take the first NN as head.
                head_tr = findFirstbreadthFirst(T[0], 'NN')
        else:
            head_tr = findFirstbreadthFirst(T[0], 'NN')

        if head_tr == None or (head_tr != None and head_tr[0] in not_allowed):
            return None, -1
        else:
            head = head_tr[0]
            idx = [pos[0] for pos in T.pos()].index(head)
            return head, idx

if __name__ == '__main__':
    import sys
    from pprint import pprint
    import os.path as osp
    sys.path.insert(0, '../..')
    from pyutils.corenlp import StanfordCoreNLP
    core = StanfordCoreNLP('../../models/stanford-corenlp-full-2015-01-29')

    # sent = "baseball man"
    # sent = 'a running person under the tree.'
    sent = 'a sandal colour teddy bear in between the other two teddys'
    parse = core.raw_parse(sent)['sentences'][0]
    parse_tree = parse['parsetree']
    t = Tree.fromstring(parse_tree)
    t.draw()
    print t
    print parse['dependencies']

    # vicente version
    head, idx = findHead(t, mode='vicente')
    print 'vicente            - head: %s, idx: %s' % (head, idx)
    # licheng version
    head, idx = findHead(t, mode='licheng')
    print 'ylc_leftNP_rightNN - head: %s, idx: %s' % (head, idx)





