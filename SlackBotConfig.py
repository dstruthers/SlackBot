import ConfigParser, os

config = ConfigParser.RawConfigParser()
config_dir = os.path.dirname(os.path.realpath(__file__))
config.read(config_dir + '/SlackBot.cfg')

SLACK_API_BASE = config.get('General', 'api_base_uri')
DEBUG = config.getboolean('General', 'debug')
