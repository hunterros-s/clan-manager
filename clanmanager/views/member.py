"""
Clan manger member view

URLs include:
/<member tag>
"""
import flask
import clanmanager

from clanmanager.utils import unix_time_to_readable


@clanmanager.app.route('/<member_tag>')
def get_member(member_tag):
    """Display /<member tag>"""
    clan_data = clanmanager.model.get_clan_data()
    members = clan_data['current_members'].keys()

    if member_tag not in members:
        flask.abort(404, f"Invalid member tag '{member_tag}' (either invalid format or tag is not a current member of the clan)")
    
    member_data = clanmanager.model.get_member(clan_data, member_tag)
    if member_data is None:
        flask.abort(500, f"Server error: data of {member_tag} is empty")

    context = {}

    context['name'] = member_data['name']
    context['tag'] = member_tag
    context['role'] = member_data['role']
    context['league'] = member_data['league']
    context['last_active'] = unix_time_to_readable(member_data['last_active'])
    context['joined'] = unix_time_to_readable(member_data['joined'])
    
    return flask.render_template("member.html", **context)