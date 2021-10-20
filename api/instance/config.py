import os
class Config(object):
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    SECRET_KEY = os.environ.get("SECRET_KEY")
