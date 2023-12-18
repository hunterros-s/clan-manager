"""Clash of Clans Clan Manager package manager."""
import flask

# Initialize the Flask app instance
app = flask.Flask(__name__)

# Import views and models (assuming they contain route handling and model definitions)
import clanmanager.views
import clanmanager.model
