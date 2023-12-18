import shared

import asyncio
import os
import time
import coc
from coc import utils

coc_client = coc.EventsClient()

"""Clan Events"""

@coc.ClanEvents.member_join()
async def on_clan_member_join(member, clan):
    coc_client.add_player_updates(member.tag)
    shared.log.info(f"{member.name} ({member.tag}) added to event listener.")
    shared.log.info(f"{member.name} has joined {clan.name}")


@coc.ClanEvents.member_leave()
async def on_clan_member_leave(member, clan):
    coc_client.remove_player_updates(member.tag)
    shared.log.info(f"{member.name} ({member.tag}) removed from event listener.")
    shared.log.info(f"{member.name} has left {clan.name}")



def timestamp(data):
    return {
        "value": data,
        "timestamp": int(time.time())
    }



async def setup_events() -> None:
    # Get the clan using its tag
    clan = await coc_client.get_clan(tag=shared.clan_tag)

    # Add clan to event listener
    coc_client.add_clan_updates(tag=shared.clan_tag)
    shared.log.info(f"{clan.name} ({clan.tag}) added to event listener.")

    # Iterate through the members and print their information
    async for member in clan.get_detailed_members():
        coc_client.add_player_updates(member.tag)
        shared.log.info(f"{member.name} ({member.tag}) added to event listener.")

    # Register all the callback functions that are triggered when an event if fired.
    coc_client.add_events(
        on_clan_member_join,
        on_clan_member_leave
    )

async def populate_clan_data() -> None:
    clan = await coc_client.get_clan(tag=shared.clan_tag)

    # get general clan member information
    shared.clan_data = {
        'name': clan.name,
        'tag': clan.tag,
        'description': clan.description,
        'badge': clan.badge.large,
        'level': clan.level,
        'location': clan.location.name,
        'type': clan.type,
        'points': clan.points,
        'builder_base_points': clan.builder_base_points,
        'capital_points': clan.capital_points,
        'member_count': clan.member_count,
        'share_link': clan.share_link,
        'current_members': {},
        'former_members': {}
    }

    # Get basic clan member information
    for member in clan.members:
        shared.clan_data['current_members'][member.tag] = {
            'name': member.name,
            'role': str(member.role),
            'league': member.league.icon.medium,
            'share_link': member.share_link,
            # Time series following:
            'exp_level': [timestamp(member.exp_level)],
            'trophies': [timestamp(member.trophies)],
            'builder_base_trophies': [timestamp(member.builder_base_trophies)],
        }

    # Get more specifc clan member information
    async for member in clan.get_detailed_members():
        # Time series following:
        member_info = shared.clan_data['current_members'][member.tag]

        def get_achievement_value(name):
            return member.get_achievement(name).value

        member_info['gold_looted'] = [timestamp(get_achievement_value("Gold Grab"))]
        member_info['elixir_looted'] = [timestamp(get_achievement_value("Elixir Escapade"))]
        member_info['dark_elixir_looted'] = [timestamp(get_achievement_value("Heroic Heist"))]
        member_info['attacks_won'] = [timestamp(get_achievement_value("Conqueror"))]
        member_info['donated'] = [timestamp(get_achievement_value("Friend in Need"))]
        member_info['spell_donated'] = [timestamp(get_achievement_value("Sharing is caring"))]
        member_info['machine_donated'] = [timestamp(get_achievement_value("Siege Sharer"))]
        member_info['war_stars'] = [timestamp(get_achievement_value("War Hero"))]
        member_info['clan_games_points'] = [timestamp(get_achievement_value("Games Champion"))]
        member_info['war_league_stars'] = [timestamp(get_achievement_value("War League Legend"))]
        member_info['capital_gold_looted'] = [timestamp(get_achievement_value("Aggressive Capitalism"))]
        member_info['clan_capital_contributions'] = [timestamp(get_achievement_value("Most Valuable Clanmate"))]

async def login() -> None:
    try:
        await coc_client.login(os.environ.get("DEV_SITE_EMAIL"),
                                os.environ.get("DEV_SITE_PASSWORD"))
    except coc.InvalidCredentials as error:
        exit(error)