import shared

import asyncio
import os
import time
import coc
from coc import utils

coc_client = None

"""Clan Events"""

# Triggered when a member joins the clan
@coc.ClanEvents.member_join()
async def on_clan_member_join(member, clan):
    #coc_client.add_player_updates(member.tag)
    #shared.log.info(f"{member.name} ({member.tag}) added to event listener.")
    shared.log.info(f"{member.name} has joined {clan.name}")
    # check former members for player, if not, create new dict for this player
    if member.tag in shared.clan_data['former_members']:
        # Move member data from former_members to current_members
        member_data = shared.clan_data['former_members'].pop(member.tag)
        shared.clan_data['current_members'][member.tag] = member_data
        shared.log.info(f"{member.name} ({member.tag}) moved to current members dict.")
    else:
        shared.log.info(f"{member.name} ({member.tag}) not found in former members dict.")

# Triggered when a member leaves the clan
@coc.ClanEvents.member_leave()
async def on_clan_member_leave(member, clan):
    #coc_client.remove_player_updates(member.tag)
    #shared.log.info(f"{member.name} ({member.tag}) removed from event listener.")
    shared.log.info(f"{member.name} has left {clan.name}")
    # Need to move this member's dict to former members
    if member.tag in shared.clan_data['current_members']:
        # Move member data from current_members to former_members
        member_data = shared.clan_data['current_members'].pop(member.tag)
        shared.clan_data['former_members'][member.tag] = member_data
        shared.log.info(f"{member.name} ({member.tag}) moved to former members dict.")
    else:
        shared.log.info(f"{member.name} ({member.tag}) not found in current members dict.")

@coc.ClanEvents.name()
async def update_clan_name(_, clan):
    shared.clan_data['name'] = clan.name
    shared.log.info(f"{clan.name} ({clan.tag}) name updated.")

@coc.ClanEvents.description()
async def update_clan_desc(_, clan):
    shared.clan_data['description'] = clan.description
    shared.log.info(f"{clan.name} ({clan.tag}) description updated.")

@coc.ClanEvents.badge()
async def update_clan_badge(_, clan):
    shared.clan_data['badge'] = clan.badge.large
    shared.log.info(f"{clan.name} ({clan.tag}) badge updated.")

@coc.ClanEvents.level()
async def update_clan_level(_, clan):
    shared.clan_data['level'] = clan.level
    shared.log.info(f"{clan.name} ({clan.tag}) level updated.")

@coc.ClanEvents.location()
async def update_clan_location(_, clan):
    shared.clan_data['location'] = clan.location.name
    shared.log.info(f"{clan.name} ({clan.tag}) location updated.")

@coc.ClanEvents.type()
async def update_clan_type(_, clan):
    shared.clan_data['type'] = clan.type
    shared.log.info(f"{clan.name} ({clan.tag}) type updated.")

@coc.ClanEvents.points()
async def update_clan_points(_, clan):
    shared.clan_data['points'] = clan.points
    shared.log.info(f"{clan.name} ({clan.tag}) points updated.")

@coc.ClanEvents.versus_points()
async def update_clan_builder_points(_, clan):
    shared.clan_data['builder_base_points'] = clan.builder_base_points
    shared.log.info(f"{clan.name} ({clan.tag}) builder base points updated.")

@coc.ClanEvents.member_count()
async def update_clan_member_count(_, clan):
    shared.clan_data['member_count'] = clan.member_count
    shared.log.info(f"{clan.name} ({clan.tag}) member count updated.")



@coc.ClanEvents.member_donations()
async def on_clan_member_donation(old_member, new_member):
    final_donated_troops = new_member.donations - old_member.donations
    shared.log.info(
        f"{new_member} of {new_member.clan} just donated {final_donated_troops} troops.")

@coc.ClanEvents.member_received()
async def on_clan_member_donation_receive(old_member, new_member):
    final_received_troops = new_member.received - old_member.received
    shared.log.info(
        f"{new_member} of {new_member.clan} just received {final_received_troops} troops.")

@coc.ClanEvents.member_role()
async def on_clan_member_role_change(old_member, new_member):
    shared.log.info(
        f"{new_member} of {new_member.clan} {old_member.role} -> {new_member.role}")

@coc.ClanEvents.member_trophies()
async def on_clan_member_trophy_change(old_member, new_member):
    shared.log.info(
        f"{new_member} of {new_member.clan} trophies went from {old_member.trophies} to {new_member.trophies}")

@coc.ClanEvents.member_versus_trophies()
async def clan_member_builder_trophies_changed(old_member, new_member):
    shared.log.info(
        f"{new_member} versus trophies changed from {old_member.builder_base_trophies} to {new_member.builder_base_trophies}")


def timestamp(data):
    return {
        "value": data,
        "timestamp": int(time.time())
    }


def setup_events():
    # Add clan to event listener
    coc_client.add_clan_updates(shared.clan_tag)
    shared.log.info(f"{shared.clan_data['name']} ({shared.clan_data['tag']}) added to event listener.")

    # we can create a list of functions and open it inside. this would give us flexibility to move the events to a different file if needed
    # Register all the callback functions that are triggered when an event if fired.
    coc_client.add_events(
        on_clan_member_join,
        on_clan_member_leave,
        update_clan_name,
        update_clan_desc,
        update_clan_badge,
        update_clan_level,
        update_clan_location,
        update_clan_type,
        update_clan_points,
        update_clan_builder_points,
        update_clan_member_count,
        on_clan_member_donation,
        on_clan_member_donation_receive,
        on_clan_member_role_change,
        on_clan_member_trophy_change,
        clan_member_builder_trophies_changed
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
    global coc_client  # Reference the global coc_client variable
    coc_client = coc.EventsClient(loop=asyncio.get_event_loop())
    try:
        await coc_client.login(os.environ.get("DEV_SITE_EMAIL"),
                                os.environ.get("DEV_SITE_PASSWORD"))
    except coc.InvalidCredentials as error:
        exit(error)

async def close_coc_client():
    if coc_client:
        await coc_client.close()