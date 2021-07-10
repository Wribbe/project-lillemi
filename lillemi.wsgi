import os
os.environ['LILLEMI_PATH_DATA'] = '/srv/http/data/project-lillemi'

from lillemi import db
db.init()
from lillemi.app import app as application
