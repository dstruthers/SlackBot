class SlackUser:
    '''Basic representation of a Slack user'''

    @staticmethod
    def from_dict(d):
        '''Creates a SlackUser object from a dictionary of attributes.
        Suitable for use with objects returned by Slack RTM API.'''

        u = SlackUser()
        u.id = d['id']
        u.username = d['name']
        u.presence = d['presence']
        if d.has_key('profile'):
            if d['profile'].has_key('email'):
                u.email = d['profile']['email']
            if d['profile'].has_key('first_name'):
                u.first_name = d['profile']['first_name']
            if d['profile'].has_key('last_name'):
                u.last_name = d['profile']['last_name']
            if d['profile'].has_key('real_name'):
                u.real_name = d['profile']['real_name']
        return u
