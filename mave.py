#-*- coding:utf-8 -*-
import os
from Queue import Queue
from janome.tokenizer import Tokenizer

import random

class Mave(object):
    def __init__(self, name='メイ'):
        self.name = name
        self.msg_que = Queue()
        self.tokenizer = Tokenizer()

        self.markov = Markov()

    def listenTo(self, message, talker):
        tokens = self.tokenizer.tokenize(message.decode('utf-8'))
        for tok in tokens:
            print '%10s (%10s) ... %s' % (tok.surface, tok.reading, tok.part_of_speech)

        self.markov.addSentence([tok.surface for tok in tokens])

        meishi_list = [tok.surface for tok in tokens 
                       if u'名詞' in tok.part_of_speech.split(',') and
                          u'一般' in tok.part_of_speech.split(',')  ]

        key = random.choice(meishi_list) if len(meishi_list) != 0 else None
        rsp = self.markov.generate(key)
        if rsp != None:
            self.msg_que.put(rsp)
        else:
            self.msg_que.put('はいはい > %s' % talker)

    def speak(self):
        if self.msg_que.empty():
            return None

        return self.msg_que.get()


class Markov(object):
    def __init__(self):
        self.dic = {}
        self.starts = set()
        self.chain_max = 30
    
    def addSentence(self, tokens):
        if len(tokens) < 3: return

        pre1, pre2 = tokens[0], tokens[1]
        self.starts.add(pre1)

        for sfx in tokens[2:]:
            self.add_suffix(pre1, pre2, sfx)
            pre1, pre2 = pre2, sfx
        else:
            self.add_suffix(pre1,pre2,u'**EOS**')

    def add_suffix(self, pre1, pre2, sfx):
        if not pre1 in self.dic:
            self.dic[pre1] = {}
        if not pre2 in self.dic[pre1]:
            self.dic[pre1][pre2] = set()
        self.dic[pre1][pre2].add(sfx)
        
    def generate(self, keyword):
        if len(self.dic) == 0: return None

        words = []

        pre1 = keyword if keyword in self.dic else random.choice(list(self.starts))
        pre2 = random.choice(self.dic[pre1].keys())

        words.append(pre1)
        words.append(pre2)

        for i in range(0, self.chain_max):
            sfx = random.choice(list(self.dic[pre1][pre2]))
            if sfx == u'**EOS**': break
                
            words.append(sfx)
            pre1, pre2 = pre2, sfx

        return ''.join([w.encode('utf-8') for w in words])
