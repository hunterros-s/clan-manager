"""
This is used to render the superlatives in index.py for index.html
"""
import flask
import clanmanager

import time

from clanmanager.utils import unix_time_to_readable, convert_to_encoded_url


def format_number(number):
    return "{:,}".format(number)


def get_best_performers(members, key):
    m = []
    for tag, member in members.items():
        series = member.get(key)
        if series is None:
            return  # this shouldn't happen but just incase
        two_weeks_ago = int(time.time()) - (60*60*24*14)
        timed_series = [stamp for stamp in series if stamp['timestamp'] >= two_weeks_ago]
        delta = timed_series[-1]['value'] - timed_series[0]['value']
        m.append({
            'name': member['name'],
            'tag': tag,
            'score': delta
        })
    sorted_m = sorted(m, key=lambda x: x['score'], reverse=True)
    return sorted_m


def get_top_performers_info(members, key, title, descriptor):
    performers = get_best_performers(members, key)
    top_info = {
        'name': title,
        'description': descriptor,
        'members': []
    }
    for member in performers[:3]:
        top_info['members'].append({
            'name': member['name'],
            'link': f"/{convert_to_encoded_url(member['tag'])}",
            'score': format_number(member['score'])
        })
    return top_info


def render_superlatives(members):
    superlatives = []

    superlatives.append(get_top_performers_info(
        members,
        'attacks_won',
        'Supreme Conqueror',
        'These formidable warriors have triumphed in the highest number of attacks, showcasing unparalleled prowess and dominance on the battlefield.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'trophies',
        'Trophy Maestro',
        'Masters of strategy, these members have amassed the most trophies, a testament to their strategic finesse and unrivaled dominance in the leagues.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'builder_base_trophies',
        'Builder\'s Sentinel',
        'These commanders have conquered the Builder Base, displaying unparalleled skill and dominance by collecting the highest number of trophies.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'gold_looted',
        'Treasure Raider',
        'Pillaging experts, these raiders have looted the most gold, showcasing exceptional prowess in acquiring wealth through successful raids.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'dark_elixir_looted',
        'Dark Elixir Overlord',
        'Experts in seizing rare resources, these marauders have claimed the most dark elixir, symbolizing mastery in extracting this elusive substance.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'donated',
        'Philanthropic Patron',
        'These generous souls have donated the most troops, embodying a spirit of selflessness and camaraderie'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'war_stars',
        'Warrior Luminary',
        'These stalwart warriors have earned the most war stars, standing as a symbol of valor and commitment in wars.'
    ))

    superlatives.append(get_top_performers_info(
        members,
        'clan_capital_contributions',
        'Capital Champion',
        'These contributors have offered the most capital gold to the clan\'s capital, demonstrating dedication and support.'
    ))

    # custom activity one
    m = []
    for tag, member in members.items():
        series = member.get("activity_series")
        two_weeks_ago = int(time.time()) - (60*60*24*14)
        timed_series = [stamp for stamp in series if stamp >= two_weeks_ago]
        pings = len(timed_series)
        m.append({
            'name': member['name'],
            'tag': tag,
            'score': pings
        })
    sorted_m = sorted(m, key=lambda x: x['score'], reverse=True)
    info = {
        'name': "Energetic Enforcer",
        'description': "These members have exhibited the most consistent activity, reflecting an unwavering dedication to the clan.",
        'members': []
    }
    for member in sorted_m[:3]:
        info['members'].append({
            'name': member['name'],
            'link': f"/{convert_to_encoded_url(member['tag'])}",
            'score': format_number(member['score'])
        })
    superlatives.append(info)

    return superlatives