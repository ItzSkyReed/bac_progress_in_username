import os
import re
import time
import logging
import json
from dataclasses import dataclass, asdict
from pathlib import Path
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] (%(levelname)s) %(name)s: %(message)s")

DEFAULT_PATH = "config.json"

@dataclass
class Config:
    delay: int = 300 # Delay between server updates
    servers: list = None # Server ids where nickname will be changed
    world_folder: str = "/path/to/world_folder"
    nickname: str = "DEFAULT_NAME"  # Your nickname without [progress]
    total_advancements: int = 1152 # Total advancement (as for BACAP 1.18.1)
    progress_pattern: str = "<NAME> [<COMPLETED_ADV>/<TOTAL_ADV>]" # <NAME>, <COMPLETED_ADV>, <TOTAL_ADV> are placeholders

    def __post_init__(self):
        if self.servers is None:
            self.servers = [419383460600348673]  # Default server

    @classmethod
    def load(cls, path: str = DEFAULT_PATH):
        global CONFIG
        config_path = Path(path)
        if config_path.exists():
            with config_path.open(encoding="utf-8") as f:
                data = json.load(f)
            return cls(**data)
        else:
            logging.info("No config file found, creating default config...")
            CONFIG = cls()
            CONFIG.save()
            return CONFIG

    def save(self, path: str = DEFAULT_PATH):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=4)

TOKEN = None



def extract_token():
    global TOKEN
    load_dotenv()
    TOKEN = os.getenv("TOKEN")


def format_progress(template, name, completed, total):
    pattern = r"<NAME>|<COMPLETED_ADV>|<TOTAL_ADV>"

    def replacer(match):
        if match.group() == "<NAME>":
            return name
        elif match.group() == "<COMPLETED_ADV>":
            return str(completed)
        elif match.group() == "<TOTAL_ADV>":
            return str(total)
        return match.group()

    return re.sub(pattern, replacer, template)


def update_nickname(nickname: str, server_id: int):
    tries = 0
    while True:
        try:
            result = requests.patch(
                url=f"https://discord.com/api/v10/guilds/{server_id}/members/@me",
                json={"nick": nickname},
                headers={"Authorization": TOKEN}
            )

            if result.status_code == 200:
                logging.info(f"Nickname successfully updated: {nickname}")
                return

            elif result.status_code == 401:
                # Unauthorized status code
                logging.fatal("Invalid (Unauthorized) discord token!")
                exit(1)

            elif result.status_code == 429:
                # rate limit status code
                rate_limit = float(result.headers["Retry-After"])
                logging.warning(f"Rate limited by Discord. Waiting {rate_limit} seconds before trying again.")
                time.sleep(rate_limit)

            elif result.status_code == 403:
                logging.fatal(f"Dont have permission to change nickname in this server: {server_id}")
                exit(1)

        except Exception as e:
            logging.error(e)

            tries += 1

            if tries >= 10:
                logging.error("Failed api call 10 times. QUITTING")
                exit(1)


def get_adv_progress(adv_name: str = "blazeandcave:bacap/advancement_legend") -> int:
    advancements_path = Path(CONFIG.world_folder) / "advancements"
    json_files = list(advancements_path.glob("*.json"))

    if not json_files:
        logging.error("Empty advancements folder!")
        return 0  # No progress

    filename = json_files[0]  # Take any JSON file

    while True:
        try:
            with filename.open("r", encoding="utf-8") as f:
                data = json.load(f)
            break  # Successfully loaded
        except (IOError, json.JSONDecodeError) as e:
            logging.warning(f"Couldn't open advancement file ({e}), retrying in 3 seconds...")
            time.sleep(3)

    logging.info(f"Advancement file {filename} loaded.")

    return len(data.get(adv_name, {}).get("criteria", {}))


def main():

    extract_token()
    if TOKEN == "<INSERT_TOKEN_HERE>" or TOKEN is None:
        logging.fatal("No token provided!")
        exit(1)

    if not Path(CONFIG.world_folder).exists():
        logging.fatal("World folder doesn't exist!")
        exit(1)

    if CONFIG.nickname == "DEFAULT_NAME":
        logging.fatal("Set up your nickname in the config!")
        exit(1)

    old_name = None

    while True:
        final_name = format_progress(CONFIG.progress_pattern, CONFIG.nickname, get_adv_progress(), CONFIG.total_advancements)

        if old_name == final_name:
            logging.info("Nothing changed since previous check")

        else:
            logging.info("Trying to updated discord nickname")
            for server in CONFIG.servers:
                logging.info(f"Updating on server {server}...")
                update_nickname(final_name, server)

        logging.info(f"Sleeping for {CONFIG.delay} seconds...")

        time.sleep(CONFIG.delay)


if __name__ == "__main__":
    CONFIG = Config.load()

    if not Path(".env").exists():
        logging.info("No .env file found, creating one...")
        with open(".env", "w") as env:
            env.write("TOKEN=<INSERT_TOKEN_HERE>\n")

    try:
        logging.info("Starting main process...")
        main()
    finally:
        print("Bye! Have a great day!!!")
