import shared
from server import start_server

import time

def main():
    start_server()

    shared.clan_data['tag'] = shared.clan_tag

    while True:
        time.sleep(1)  # Some sort of action to keep the main thread active


if __name__ == "__main__":
    main()