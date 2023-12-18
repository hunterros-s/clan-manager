"""Clan manager configuration."""

import pathlib

# The Clash of Clans clan tag being managed
CLAN_TAG = "#JGJLULUG"

# Root URL for the application
APPLICATION_ROOT = '/'

# Resolve the parent directory of the current file (this configuration file)
CLANMANAGER_ROOT = pathlib.Path(__file__).resolve().parent.parent

# File path for the clan data database (clandata.json) using the resolved path
DATABASE_FILENAME = CLANMANAGER_ROOT / 'var' / 'clandata.json'
