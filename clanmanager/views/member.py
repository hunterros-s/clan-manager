"""
Clan manger member view

URLs include:
/<member tag excluding #>/
"""
import flask
import clanmanager

@clanmanager.app.route('/<member_tag>')
def get_member(member_tag):
    return f"{member_tag}"