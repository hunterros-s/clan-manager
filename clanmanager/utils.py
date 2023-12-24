"""Utility functions."""
import flask
import clanmanager

from datetime import datetime

import urllib.parse


def convert_to_encoded_url(input_string):
    encoded_string = urllib.parse.quote(input_string, safe='')
    return encoded_string

def unix_to_datetime(unix_time):
    timestamp = datetime.fromtimestamp(unix_time)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

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
    elif seconds < 259200:  # 3 days
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif seconds < 2592000:  # Approximately 30 days
        days = int(seconds // 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")