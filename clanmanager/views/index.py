"""
Clan manger index view

URLs include:
/
"""
import flask
import clanmanager
from datetime import datetime

import urllib.parse

def convert_to_encoded_url(input_string):
    encoded_string = urllib.parse.quote(input_string, safe='')
    return encoded_string

def unix_time_to_readable(unix_time):
    current_time = datetime.now()
    timestamp = datetime.fromtimestamp(unix_time)
    time_difference = current_time - timestamp

    seconds = time_difference.total_seconds()

    if seconds < 60:
        return "recently"
    elif seconds < 360:
        return "a few minutes ago"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 2592000:  # Approximately 30 days
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")


@clanmanager.app.route('/')
def index():
    """Display / route."""
    clan_data = clanmanager.model.get_clan_data()
    if not clan_data:
        flask.abort(404)
    
    context = {
        'clan': {
            'name': clan_data['name'],
            'tag': clan_data['tag'],
            'description': clan_data['description'],
            'badge': clan_data['badge'],
            'level': clan_data['level'],
            'location': clan_data['location'],
            'type': clan_data['type'],
            'points': clan_data['points'],
            'builder_base_points': clan_data['builder_base_points'],
            'member_count': clan_data['member_count'],
            'share_link': clan_data['share_link']
        },
        'members': []
    }

    mems = []
    for tag, member in clan_data['current_members'].items():
        m = {
            'sort_by': member['last_active'],
            'name': member['name'],
            'tag': tag,
            'joined': unix_time_to_readable(member['joined']),
            'last_active': unix_time_to_readable(member['last_active']),
            'role': member['role'],
            'league': member['league'],
            'share_link': member['share_link'],
            'member_link': f"/{convert_to_encoded_url(tag)}"
        }
        mems.append(m)
    
    sorted_mems = sorted(mems, key=lambda x: x['sort_by'], reverse=True)

    context['members'] = sorted_mems


    
    return flask.render_template("index.html", **context)