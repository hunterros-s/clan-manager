"""
Clan manger member view

URLs include:
/<member tag>
"""
import flask
import clanmanager
import json

from clanmanager.utils import unix_time_to_readable, unix_to_datetime


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
    context['share_link'] = member_data['share_link']
    context['last_active'] = unix_time_to_readable(member_data['last_active'])
    context['joined'] = unix_time_to_readable(member_data['joined'])

    data_sets = []

    # trophies
    trophies = {
        'name': 'Trophies',
        'yaxis': 'Trophies',
        'linecolor': 'rgb(253, 218, 42)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['trophies']],
        'y': [x['value'] for x in member_data['trophies']]
    }
    data_sets.append(trophies)

    # builder_base_trophies
    builder_base_trophies = {
        'name': 'Builder Base Trophies',
        'yaxis': 'Builder Base Trophies',
        'linecolor': 'rgb(148, 0, 102)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['builder_base_trophies']],
        'y': [x['value'] for x in member_data['builder_base_trophies']]
    }
    data_sets.append(builder_base_trophies)

    # gold_looted
    gold_looted = {
        'name': 'Gold Looted',
        'yaxis': 'Gold Looted',
        'linecolor': 'rgb(253, 245, 27)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['gold_looted']],
        'y': [x['value'] for x in member_data['gold_looted']]
    }
    data_sets.append(gold_looted)

    # elixir_looted
    elixir_looted = {
        'name': 'Elixir Looted',
        'yaxis': 'Elixir Looted',
        'linecolor': 'rgb(167, 42, 253)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['elixir_looted']],
        'y': [x['value'] for x in member_data['elixir_looted']]
    }
    data_sets.append(elixir_looted)

    # dark_elixir_looted
    dark_elixir_looted = {
        'name': 'Dark Elixir Looted',
        'yaxis': 'Dark Elixir Looted',
        'linecolor': 'rgb(80, 0, 160)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['dark_elixir_looted']],
        'y': [x['value'] for x in member_data['dark_elixir_looted']]
    }
    data_sets.append(dark_elixir_looted)

    # attacks_won
    attacks_won = {
        'name': 'Attacks won',
        'yaxis': 'Attacks won',
        'linecolor': 'rgb(254, 14, 14)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['attacks_won']],
        'y': [x['value'] for x in member_data['attacks_won']]
    }
    data_sets.append(attacks_won)

    # donated
    donated = {
        'name': 'Troops donated',
        'yaxis': 'Troops donated',
        'linecolor': 'rgb(13, 139, 254)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['donated']],
        'y': [x['value'] for x in member_data['donated']]
    }
    data_sets.append(donated)

    # war_stars
    war_stars = {
        'name': 'War stars',
        'yaxis': 'War Stars',
        'linecolor': 'rgb(219, 244, 26)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['war_stars']],
        'y': [x['value'] for x in member_data['war_stars']]
    }
    data_sets.append(war_stars)

    # clan_games_points
    clan_games_points = {
        'name': 'Clan game points',
        'yaxis': 'Clan game points',
        'linecolor': 'rgb(26, 244, 51)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['clan_games_points']],
        'y': [x['value'] for x in member_data['clan_games_points']]
    }
    data_sets.append(clan_games_points)

    # capital_gold_looted
    capital_gold_looted = {
        'name': 'Capital gold looted',
        'yaxis': 'Capital gold looted',
        'linecolor': 'rgb(255, 251, 16)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['capital_gold_looted']],
        'y': [x['value'] for x in member_data['capital_gold_looted']]
    }
    data_sets.append(capital_gold_looted)

    # clan_capital_contributions
    clan_capital_contributions = {
        'name': 'Clan capital contributions',
        'yaxis': 'Clan capital contributions',
        'linecolor': 'rgb(255, 251, 16)',
        'x': [unix_to_datetime(x['timestamp']) for x in member_data['clan_capital_contributions']],
        'y': [x['value'] for x in member_data['clan_capital_contributions']]
    }
    data_sets.append(clan_capital_contributions)


    context['plot_data'] = data_sets

    print(context['plot_data'])

    return flask.render_template('member.html', **context)