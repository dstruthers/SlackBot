class SlackEvent:
    '''Basic representation of a Slack event object'''

    @staticmethod
    def from_dict(d):
        '''Creates a SlackEvent object from a dictionary of attributes.
        Suitable for use with objects returned by WebSocket API'''

        e = SlackEvent()
        e.type = d['type']

        if d['type'] == 'message':
            e.ts = float(d['ts'])
            e.user = d['user']
            e.channel = d['channel']
            e.text = d['text']
        elif d['type'] == 'presence_change':
            e.user = d['user']
            e.presence = d['presence']
        return e
