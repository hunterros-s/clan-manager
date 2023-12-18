import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

clan_tag = os.environ.get("CLAN_TAG")
if clan_tag is None:
    log.info("The 'CLAN_TAG' environment variable is not set.")
    log.info("- Windows Command Prompt: set CLAN_TAG=#your_clan_tag_here")
    log.info("- Windows PowerShell: $env:CLAN_TAG = '#your_clan_tag_here'")
    log.info("- Linux/macOS Terminal: export CLAN_TAG=#your_clan_tag_here")
    exit(1)
else:
    log.info(f"The 'CLAN_TAG' environment variable is: {clan_tag}")

clan_data = {}