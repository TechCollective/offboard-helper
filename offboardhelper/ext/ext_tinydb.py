import os
from tinydb import TinyDB
from cement.utils import fs

def extend_tinydb(app):
    app.log.debug('extending todo application with tinydb')
    db_file = "./project.json"
    
    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.debug('tinydb database file is: %s' % db_file)
    
    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))
    app.log.debug("Tinydb extended added")
    
def load(app):
    app.hook.register('project_dir_setup', extend_tinydb)