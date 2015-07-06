class SlackChannel:
    '''Basic representation of a Slack chat channel'''

    @staticmethod
    def from_dict(d):
        '''Creates a SlackChannel object from a dictionary of attributes.
        Suitable for use with objects return by Slack RTM API.'''

        c = SlackChannel()
        c.id = d['id']
        c.is_archived = d['is_archived']
        c.is_general = d['is_general']
        if d.has_key('members'):
            c.members = d['members']
        c.name = d['name']
        if d.has_key('topic') and d['topic'].has_key('value'):
            c.topic = d['topic']['value']
        return c
