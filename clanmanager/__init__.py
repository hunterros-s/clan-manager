"""Clash of Clans Clan Manager package manager."""
import flask

app = flask.Flask(__name__)

import clanmanager.views
import clanmanager.model

if __name__ == '__main__':
    app.run(debug=True)