import shared
import asyncio

from server import start_server
from model import import_data, save_data, save_data_periodically

from cocapi import login, setup_events, close_coc_client
from cocapi import get_clan_data, set_clan_information, reinit_members


async def main():
    await login()

    import_data()

    clan = await get_clan_data()
    set_clan_information(clan)

    await reinit_members(clan)

    save_data()

    setup_events()

    shared.log.info("Starting data save routine. Saving data every 5 minutes...")
    save_data_periodically()


if __name__ == "__main__":
    start_server()

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
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