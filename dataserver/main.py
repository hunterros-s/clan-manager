import shared
import asyncio

from server import start_server
from model import import_data, save_data

from cocapi import login
from cocapi import populate_clan_data

import time

async def main():
    start_server()

    await login()

    loaded = import_data()

    if not loaded:
        shared.log.info("Clan info file not found, populating from scratch.")
        await populate_clan_data()
        save_data()


    while True:
        time.sleep(1)  # Some sort of action to keep the main thread active


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())