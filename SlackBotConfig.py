import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('SlackBot.cfg')

SLACK_API_BASE = config.get('General', 'api_base_uri')
DEBUG = config.getboolean('General', 'debug')
