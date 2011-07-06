# -*- coding: utf-8 -*-

"""
dash.core
~~~~~~~~~

Dashboard.
"""


import redi

from flask import (
    request, session, redirect, url_for,
    abort, render_template, flash, Flask, g
)

app = Flask(__name__)
app.debug = True


from .db import redis_connect
from .views import index

app.register_blueprint(index)



@app.before_request
def before_request():

    # redis connect
    if not getattr(g, 'r', None):
        g.r = redis_connect()

        redi.config.init(r=g.r)



if __name__ == '__main__':
    app.run()