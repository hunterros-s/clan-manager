import shared

import asyncio
import os
import time
import coc
from coc import utils

coc_client = None

def move_former_to_current(tag):
    # Move member data from former_members to current_members
    member_data = shared.clan_data['former_members'].pop(tag)
    shared.clan_data['current_members'][tag] = member_data
    shared.log.info(f"{member_data['name']} ({tag}) moved to current members dict.")

def move_current_to_former(tag):
    # Move member data from current_members to former_members
    member_data = shared.clan_data['current_members'].pop(tag)
    shared.clan_data['former_members'][tag] = member_data
    shared.log.info(f"{member_data['name']} ({tag}) moved to former members dict.")

def mark_activity(tag):
    member = shared.clan_data['current_members'][tag]
    t = int(time.time())
    member['last_active'] = t
    member['activity_series'].append(t)
    shared.log.info(
        f"{member['name']} marked active.")

"""CLAN EVENTS"""

# Triggered when a member joins the clan
@coc.ClanEvents.member_join()
async def on_clan_member_join(member, clan):
    coc_client.add_player_updates(member.tag)
    shared.log.info(f"{member.name} ({member.tag}) added to event listener.")
    shared.log.info(f"{member.name} has joined {clan.name}")
    # check former members for player, if not, create new dict for this player
    d_member = await get_detailed_member(member)
    if member.tag in shared.clan_data['former_members']:
        shared.log.info(f"A former member has rejoined, using old dict and updating.")
        move_former_to_current(member.tag)
        init_member(d_member)
    else:
        shared.log.info(f"Creating new member dict for {member.name} ({member.tag})")
        init_member(d_member, True)

# Triggered when a member leaves the clan
@coc.ClanEvents.member_leave()
async def on_clan_member_leave(member, clan):
    coc_client.remove_player_updates(member.tag)
    shared.log.info(f"{member.name} ({member.tag}) removed from event listener.")
    shared.log.info(f"{member.name} has left {clan.name}")
    # Need to move this member's dict to former members
    if member.tag in shared.clan_data['current_members']:
        move_current_to_former(member.tag)
    else:
        # This is an error. shouldn't happen.
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
    #This changes all the time for some reason so I'm not going to log a message

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

@coc.ClanEvents.builder_base_points()
async def update_clan_builder_points(_, clan):
    shared.clan_data['builder_base_points'] = clan.builder_base_points
    shared.log.info(f"{clan.name} ({clan.tag}) builder base points updated.")

@coc.ClanEvents.member_count()
async def update_clan_member_count(_, clan):
    shared.clan_data['member_count'] = clan.member_count
    shared.log.info(f"{clan.name} ({clan.tag}) member count updated.")

@coc.ClanEvents.member_role()
async def on_clan_member_role_change(old_member, new_member):
    shared.log.info(
        f"{new_member} of {new_member.clan} {old_member.role} -> {new_member.role}")
    shared.clan_data[new_member.tag]['role'] = new_member.role

"""PLAYER EVENTS"""

@coc.PlayerEvents.name()
async def update_player_name(old, player):
    shared.clan_data['current_members'][player.tag]['name'] = player.name
    shared.log.info(
        f"{old.name} is now known as {player.name} ({player.tag})")
    mark_activity(member.tag)

@coc.PlayerEvents.donations()
async def update_player_donation(old, member):
    final_donated_troops = member.donations - old.donations
    shared.log.info(
        f"{member} of {member.clan} just donated {final_donated_troops} troops.")
    shared.clan_data['current_members'][member.tag]['donated'].append(
        {
            'value': member.get_achievement("Friend in Need").value,
            'timestamp': int(time.time())
        }
    )
    shared.clan_data['current_members'][member.tag]['spell_donated'].append(
        {
            'value': member.get_achievement("Sharing is caring").value,
            'timestamp': int(time.time())
        }
    )
    shared.clan_data['current_members'][member.tag]['machine_donated'].append(
        {
            'value': member.get_achievement("Siege Sharer").value,
            'timestamp': int(time.time())
        }
    )
    mark_activity(member.tag)

@coc.PlayerEvents.trophies()
async def update_player_trophies(old, member):
    shared.log.info(
        f"{member} trophies changed from {old.trophies} to {member.trophies}")
    shared.clan_data['current_members'][member.tag]['trophies'].append(
        {
            'value': member.trophies,
            'timestamp': int(time.time())
        }
    )

@coc.PlayerEvents.attack_wins()
async def update_player_attacks(old, member):
    final_wins = member.attack_wins - old.attack_wins
    shared.log.info(
        f"{member} of {member.clan} just won {final_wins} attack(s).")
    shared.clan_data['current_members'][member.tag]['attacks_won'].append(
        {
            'value': member.get_achievement("Conqueror").value,
            'timestamp': int(time.time())
        }
    )
    shared.clan_data['current_members'][member.tag]['gold_looted'].append(
        {
            'value': member.get_achievement("Gold Grab").value,
            'timestamp': int(time.time())
        }
    )
    shared.clan_data['current_members'][member.tag]['elixir_looted'].append(
        {
            'value': member.get_achievement("Elixir Escapade").value,
            'timestamp': int(time.time())
        }
    )
    shared.clan_data['current_members'][member.tag]['dark_elixir_looted'].append(
        {
            'value': member.get_achievement("Heroic Heist").value,
            'timestamp': int(time.time())
        }
    )
    mark_activity(member.tag)

@coc.PlayerEvents.builder_base_trophies()
async def update_player_builder_base_trophies(old, member):
    shared.log.info(
        f"{member} builder base trophies changed from {old.builder_base_trophies} to {member.builder_base_trophies}")
    shared.clan_data['current_members'][member.tag]['builder_base_trophies'].append(
        {
            'value': member.get_achievement("Champion Builder").value,
            'timestamp': int(time.time())
        }
    )
    mark_activity(member.tag)

@coc.PlayerEvents.war_stars()
async def update_player_war_stars(old, member):
    shared.log.info(
        f"{member} war stars changed from {old.war_stars} to {member.war_stars}")
    shared.clan_data['current_members'][member.tag]['war_stars'].append(
        {
            'value': member.war_stars,
            'timestamp': int(time.time())
        }
    )
    old_war_league_stars = old.get_achievement("War League Legend").value
    new_war_league_stars = member.get_achievement("War League Legend").value
    if new_war_league_stars != old_war_league_stars:
        shared.log.info(
            f"{member.name}'s war league stars {old_war_league_stars} -> {new_war_league_stars}")
        shared.clan_data['current_members'][member.tag]['war_league_stars'].append(
            {
                'value': new_war_league_stars,
                'timestamp': int(time.time())
            }
        )
    mark_activity(member.tag)

@coc.PlayerEvents.achievement_change()
async def general_achievement_change(old_member, member, achievement):
    if achievement.name == "Games Champion":
        old = old_member.get_achievement("Games Champion").value
        new = member.get_achievement("Games Champion").value
        if new != old:
            shared.log.info(
                f"{member.name}'s clan game points {old} -> {new}")
            shared.clan_data['current_members'][member.tag]['clan_games_points'].append(
                {
                    'value': new,
                    'timestamp': int(time.time())
                }
            )
            mark_activity(member.tag)
    elif achievement.name == "Aggressive Capitalism":
        old = old_member.get_achievement("Aggressive Capitalism").value
        new = member.get_achievement("Aggressive Capitalism").value
        if new != old:
            shared.log.info(
                f"{member.name}'s capital gold looted {old} -> {new}")
            shared.clan_data['current_members'][member.tag]['capital_gold_looted'].append(
                {
                    'value': new,
                    'timestamp': int(time.time())
                }
            )
            mark_activity(member.tag)
    elif achievement.name == "Most Valuable Clanmate":
        old = old_member.get_achievement("Most Valuable Clanmate").value
        new = member.get_achievement("Most Valuable Clanmate").value
        if new != old:
            shared.log.info(
                f"{member.name}'s clan capital contributions {old} -> {new}")
            shared.clan_data['current_members'][member.tag]['clan_capital_contributions'].append(
                {
                    'value': new,
                    'timestamp': int(time.time())
                }
            )
            mark_activity(member.tag)





def timestamp(data):
    return {
        "value": data,
        "timestamp": int(time.time())
    }


async def setup_events():
    # Add clan to event listener
    coc_client.add_clan_updates(shared.clan_tag)
    shared.log.info(f"{shared.clan_data['name']} ({shared.clan_data['tag']}) added to event listener.")

    # add members to event listener
    clan = await coc_client.get_clan(shared.clan_tag)
    for member in clan.members:
        shared.log.info(
            f"{member.name} ({member.tag}) of {member.clan} added to event listener.")
        coc_client.add_player_updates(member.tag)

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
        on_clan_member_role_change,
        update_player_name,
        update_player_donation,
        update_player_trophies,
        update_player_attacks,
        update_player_builder_base_trophies,
        update_player_war_stars,
        general_achievement_change
    )

def set_clan_information(clan):
    shared.clan_data['name'] = clan.name
    shared.clan_data['tag'] = clan.tag
    shared.clan_data['description'] = clan.description
    shared.clan_data['badge'] = clan.badge.large
    shared.clan_data['level'] = clan.level
    shared.clan_data['location'] = clan.location.name
    shared.clan_data['type'] = clan.type
    shared.clan_data['points'] = clan.points
    shared.clan_data['builder_base_points'] = clan.builder_base_points
    shared.clan_data['member_count'] = clan.member_count
    shared.clan_data['share_link'] = clan.share_link

    if 'current_members' not in shared.clan_data:
        shared.clan_data['current_members'] = {}

    if 'fomer_members' not in shared.clan_data:
        shared.clan_data['former_members'] = {}


async def get_clan_data():
    return await coc_client.get_clan(tag=shared.clan_tag)


# takes basic member and returns detailed member. see more info in the coc.py documentation
async def get_detailed_member(member):
    return await coc_client.get_player(player_tag=member.tag)


# this has to be a detailed member. doesn't work for member object from clan update
def init_member(detailed_member, new_member=False):
    if new_member:
        shared.clan_data['current_members'][detailed_member.tag] = {}

    member_data = shared.clan_data['current_members'][detailed_member.tag]

    member_data['name'] = detailed_member.name

    if new_member:
        member_data['joined'] = int(time.time())
        member_data['last_active'] = int(time.time())
        member_data['activity_series'] = [int(time.time())]

    member_data['role'] = str(detailed_member.role)
    member_data['league'] = detailed_member.league.icon.medium
    member_data['share_link'] = detailed_member.share_link

    # time series
    def update_timeseries(key, achievement):
        if key not in member_data:
            member_data[key] = [{
                "value": detailed_member.get_achievement(achievement).value,
                "timestamp": int(time.time())
            }]
            return
        most_recent = member_data[key][-1]
        achievement_value = detailed_member.get_achievement(achievement).value
        if most_recent['value'] != achievement_value:
            shared.log.info(f"{detailed_member.name} ({detailed_member.tag}) {key} updated.")
            member_data[key].append({
                "value": achievement_value,
                'timestamp': int(time.time())
            })

    update_timeseries('trophies', "Sweet Victory!")
    update_timeseries('builder_base_trophies', "Champion Builder")
    update_timeseries('gold_looted', "Gold Grab")
    update_timeseries('elixir_looted', "Elixir Escapade")
    update_timeseries('dark_elixir_looted', "Heroic Heist")
    update_timeseries('attacks_won', "Conqueror")
    update_timeseries('donated', "Friend in Need")
    update_timeseries('spell_donated', "Sharing is caring")
    update_timeseries('machine_donated', "Siege Sharer")
    update_timeseries('war_stars', "War Hero")
    update_timeseries('clan_games_points', "Games Champion")
    update_timeseries('war_league_stars', "War League Legend")
    update_timeseries('capital_gold_looted', "Aggressive Capitalism")
    update_timeseries('clan_capital_contributions', "Most Valuable Clanmate")

# Reinitialize members from the loaded data
async def reinit_members(clan):
    async for member in clan.get_detailed_members():
        if member.tag in shared.clan_data['former_members']:
            move_former_to_current(member.tag)

        new_member = False
        if member.tag not in shared.clan_data['current_members']:
            new_member = True
        
        init_member(member, new_member)
    
    # need to move members that are no longer in the clan to former members.
    tags = [member.tag for member in clan.members]
    formers = [tag for tag in shared.clan_data['current_members'].keys() if tag not in tags]
    for tag in formers:
        shared.log.info(f"{shared.clan_data['current_members'][tag]['name']} ({tag}) no longer in the clan. Moving to former members.")
        move_current_to_former(tag)


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