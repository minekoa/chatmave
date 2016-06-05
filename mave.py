#-*- coding:utf-8 -*-
from Queue import Queue
from janome.tokenizer import Tokenizer
from markov_responder import Markov

class Mave(object):
    def __init__(self, name='メイ'):
        self.name = name
        self.msg_que = Queue()
        self.tokenizer = Tokenizer()

        self.markov = Markov(ngram=2)

    def listenTo(self, message, talker):
        tokens = self.tokenizer.tokenize(message.decode('utf-8'))
        for tok in tokens:
            print '%10s (%10s) ... %s' % (tok.surface, tok.reading, tok.part_of_speech)

        self.markov.learn(tokens)

        meishi_list = [tok.surface for tok in tokens 
                       if u'名詞' in tok.part_of_speech.split(',') and
                          ((u'一般' in tok.part_of_speech.split(',') and  not u'あ' <= tok.surface[0] <= u'ん')
                           or u'固有名詞' in tok.part_of_speech.split(','))]

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

