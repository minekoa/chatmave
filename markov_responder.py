#-*- coding:utf-8 -*-
import random
import json

class Markov(object):
    def __init__(self, ngram):
        self.dic = {}
        self.starts = set()
        self.ngram = ngram
        self.chain_max = 80

    #----------------------------------------
    # 学習
    #----------------------------------------
    
    def learn(self, tokens):
        # 文ごとに分離
        sentence_list = []
        buf = []
        for tok in tokens:
            buf.append(tok)
            if (u'句点' in tok.part_of_speech.split(',') or
                tok.surface == u'！' or
                tok.surface == u'？'):
                sentence_list.append(buf)
                buf = []
        else:
            if len(buf) != 0:
                sentence_list.append(buf)

        # センテンスを登録
        for sentence in sentence_list:
            self._add_sentence([tok.surface for tok in sentence])

    def _add_sentence(self, tokens):
        if len(tokens) < (self.ngram +1): return

        pre_list = tokens[:self.ngram]
        self.starts.add(pre_list[0])

        for sfx in tokens[self.ngram:]:
            self._add_suffix(pre_list, sfx)
            pre_list = pre_list[1:] + [sfx]
        else:
            self._add_suffix(pre_list, u'**EOS**')

    def _add_suffix(self, ngram_tokens, sfx):
        print 'add:[', 
        for t in ngram_tokens: print '(%s)' % t,
        print '-> (%s) ]' % sfx

        dic_cur = self.dic
        for tok in ngram_tokens[:-1]:
            if not tok in dic_cur:
                dic_cur[tok] = {}
            dic_cur = dic_cur[tok]

        if not ngram_tokens[-1] in dic_cur:
            dic_cur[ngram_tokens[-1]] = []
        
        dic_cur[ngram_tokens[-1]].append(sfx)
        
    #----------------------------------------
    # 文の生成
    #----------------------------------------

    def generate(self, keyword):
        if len(self.dic) == 0: return None
       
        # 初期キーの作成
        pre1 = keyword if keyword in self.dic else random.choice(list(self.starts))
        pre_list = self._get_first_prefix(pre1)

        # 返答生成バッファーの初期化
        words = []
        for w in pre_list: words.append(w)

        # 文書生成
        for i in range(0, self.chain_max):
            sfx = self._get_suffix(pre_list)
            if sfx == u'**EOS**': break
            words.append(sfx)
            pre_list = pre_list[1:] + [sfx]

        print len(words), '(msg)'
        return ''.join([w.encode('utf-8') for w in words])

    def _get_first_prefix(self, first_word):
        words = []
        words.append(first_word)

        dic_cur = self.dic
        for i in range(0, self.ngram-1):
            key = words[i]
            words.append(random.choice(dic_cur[key].keys()))
            dic_cur = dic_cur[key]
        return words

    def _get_suffix(self, prefix_list):
        dic_cur = self.dic
        for key in prefix_list:
            dic_cur = dic_cur[key]
        return random.choice( dic_cur )

    #----------------------------------------
    # 永続化
    #----------------------------------------
    def load(self, fname):
        self._load_markov(fname)
        self._load_starts(fname+'.starts')

    def _load_markov(self, fname):
        with open(fname,'r') as f:
            self.dic = json.loads(f.read(), "utf-8")

    def _load_starts(self, fname):
        with open(fname,'r') as f:
            self.starts = set(json.loads(f.read(), "utf-8"))

    def save(self, fname):
        self._save_markov(fname)
        self._save_starts(fname+'.starts')

    def _save_markov(self, fname):
        txt = json.dumps(self.dic,
                         ensure_ascii=False,
                         indent=1,
                         sort_keys=True)
        with open(fname, 'w') as  f:
            f.write(txt.encode('utf-8'))

    def _save_starts(self, fname):
        txt = json.dumps(list(self.starts),
                         ensure_ascii=False,
                         indent=1,
                         sort_keys=True)
        with open(fname, 'w') as  f:
            f.write(txt.encode('utf-8'))


