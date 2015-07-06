import json, re, urllib2, websocket
from time import sleep, time

from SlackBotConfig import *
from SlackUser import *
from SlackChannel import *
from SlackEvent import *
from SlackBotError import *

class SlackBot:
    '''Uses Slack RTM and WebSocket APIs to provide basic slack bot
    functionality'''

    def __init__(self, api_token):
        '''SlackBot constructor'''
        self.api_token = api_token
        self.event_listeners = {}
        self.message_id = 0
        self.show_typing = False
        self.command_prefix = '!'
        self.commands = {}
        self.start_time = time()

    def add_event_listener(self, type, fn):
        '''Add high level event listener'''
        if not self.event_listeners.has_key(type):
            self.event_listeners[type] = []
        self.event_listeners[type].append(fn)

    def add_command(self, keyword, fn):
        '''Add bot command'''
        self.commands[keyword] = fn

    def say(self, channel_id, text):
        if self.show_typing:
            for i in range(0, 2):
                msg = json.dumps({'id': self.next_message_id(),
                                  'type': 'typing',
                                  'channel': channel_id})
                self.ws.send(msg)
                sleep(1)
                
        msg = json.dumps({'id': self.next_message_id(),
                          'type': 'message',
                          'channel': channel_id,
                          'text': text})
        self.ws.send(msg)

    def next_message_id(self):
        '''Returns unique id for use in sending messages'''
        self.message_id += 1
        return self.message_id

    @staticmethod
    def rtm_call(endpoint, **args):
        '''Make Slack API call via RTM protocol'''
        params = ''
        for key in args:
            if params: params += '&'
            params += key + '=' + args[key]
        url = SLACK_API_BASE + endpoint + '?' + params
        result = json.loads(urllib2.urlopen(url).read())
        return result

    # Child classes of SlackBot may wish to override these methods
    def on_open(self, ws): pass
    def on_message(self, ws, message): pass
    def on_error(self, ws, error): pass
    def on_close(self, ws): pass

    def run(self):
        def on_open(ws):
            self.on_open(ws)
            if self.event_listeners.has_key('open'):
                for fn in self.event_listeners['open']:
                    fn(self)

        def on_message(ws, message):
            if DEBUG:
                print message

            self.on_message(ws, message)
            e = SlackEvent.from_dict(json.loads(message))

            if e.type == 'message' and e.ts < self.start_time:
                if DEBUG:
                    print 'Skipping old message:', message
                return
            
            if self.event_listeners.has_key(e.type):
                for fn in self.event_listeners[e.type]:
                    fn(self, e)

            if len(self.commands) > 0 and e.type == 'message':
                for keyword in self.commands:
                    if re.search(r'^%s%s\b' % (self.command_prefix, keyword), e.text):
                        if DEBUG:
                            print message
                        self.commands[keyword](self, e)
                    
        def on_error(ws, error):
            self.on_error(ws, error)
        def on_close(ws):
            self.on_close(ws)

        start_result = SlackBot.rtm_call('rtm.start', token=self.api_token)
        if start_result['ok']:
            self.user_id = start_result['self']['id']
            self.user_username = start_result['self']['name']
            self.user_prefs = start_result['self']['prefs']
            self.users = []
            for user in start_result['users']:
                self.users.append(SlackUser.from_dict(user))

            self.channels = []
            for channel in start_result['channels']:
                self.channels.append(SlackChannel.from_dict(channel))   


            self.ws = websocket.WebSocketApp(start_result['url'],
                                             on_message = on_message,
                                             on_error = on_error,
                                             on_close = on_close,
                                             on_open = on_open)

            websocket.enableTrace(DEBUG)
            self.ws.run_forever()
        else:
            raise SlackBotError('Could not initiate RTM session')
