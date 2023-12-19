import shared
import asyncio

from server import start_server
from model import import_data, save_data

from cocapi import login, populate_clan_data, setup_events, close_coc_client


async def main():
    start_server()

    await login()

    loaded = import_data()

    if not loaded:
        shared.log.info("Clan info file not found, populating from scratch.")
        await populate_clan_data()
        save_data()

    setup_events()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        loop.run_until_complete(close_coc_client())  # Close the coc_client session
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()