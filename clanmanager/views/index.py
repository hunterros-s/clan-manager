"""
Clan manger index view

URLs include:
/
"""
import flask
import clanmanager


@clanmanager.app.route('/')
def index():
    """Display / route."""
    context = {}
    return flask.render_template("index.html", **context)