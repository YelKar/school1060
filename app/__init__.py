"""Creating app

creating app object
adding configuration for app
"""
from flask import Flask, send_from_directory

from .config import Config
from .constants import CONTEXT_CONSTANTS

import os


app = Flask(__name__)
app.config.from_object(Config)
app.context_processor(lambda: CONTEXT_CONSTANTS)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               "img/favicon.ico", mimetype='image/vnd.microsoft.icon')


from .views import main_views
