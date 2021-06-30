import os
os.environ['LILLEMI_PATH_DATA'] = '/srv/http/data/project-lillemi-staging'

from lillemi.app import app as application
