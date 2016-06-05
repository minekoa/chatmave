#-*- coding:utf-8 -*-
import websocket
import mave
import time
import sys, traceback

class MaveProxy(object):
    def __init__(self):
        self.mave = mave.Mave(u'メイ')
        self.mave.wakeUp()

    def connectTo(self, url):
        ws = websocket.WebSocketApp(url,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.run_forever()        

    def on_error(self, ws, error):
        print '!!ERROR!!'
        print error

    def on_message(self, ws, message):
        try:
            print ">",message
            talker, filters, cmds, talk = self.parse_message(message)
            if talker == self.mave.name.encode('utf-8'):
                return

            self.mave.listenTo(talk, talker)
            resp = self.mave.speak()
            if resp != None:
                time.sleep(0.5)
                self.send_message(ws, resp, filters)

        except Exception as e:
            print e
            print '-'*60
            traceback.print_exc(file=sys.stdout)

    def on_close(self, ws):
        self.mave.goToBed()
        print '!!CLOSED!!'

    def parse_message(self, message):
        lst = [t.strip() for t in message.split(';')]
        talker   = lst[0]
        filters  = [t for t in lst if len(t) != 0 and t[0] == '#']
        commands = [t for t in lst if len(t) != 0 and t[0] == '!']
        talk     = ';'.join([t for t in lst[1:] if len(t) != 0 and t[0] != '#' and t[0] != '!'])
        return (talker, filters, commands, talk)

    def send_message(self, ws, message, filters):
        header = ';'.join([self.mave.name.encode('utf-8')] + filters)
        ws.send('%s;%s' % (header, message))

if __name__ == '__main__':
    mave_pxy = MaveProxy()
    mave_pxy.connectTo('ws://192.168.42.1:8080/chat')
