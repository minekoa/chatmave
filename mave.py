#-*- coding:utf-8 -*-
import os
from Queue import Queue

class Mave(object):
    def __init__(self, name='メイ'):
        self.name = name
        self.msg_que = Queue()

    def listenTo(self, message, talker):
        self.msg_que.put('はいはい > %s' % talker)

    def speak(self):
        if self.msg_que.empty():
            return None

        return self.msg_que.get()

