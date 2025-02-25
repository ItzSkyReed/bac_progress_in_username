import os
import time
import logging
import json
import requests

logging.basicConfig(level = logging.INFO, format = "[%(asctime)s] (%(levelname)s) %(name)s: %(message)s")

# delay in seconds
delay = 5 * 60

# server ids, where you want to change your username
servers = [419383460600348673]

# your nickname
# CHANGE THIS
# get_adv_progress function (INSIDE CURLY BRACES BECAUSE ITS AN F-STRING) needs advancement id and it will return the number of completed criteria
# fill advancement totals yourself
get_nickname = lambda: f"Name [{get_adv_progress('blazeandcave:bacap/advancement_legend')}/idk]"

# YOUR DISCORD TOKEN </3
token = ""

# full path to world folder
world_folder = "/path/to/world_folder"

if not os.path.isdir(world_folder):
    print("bruh")
    exit(1)

api_url = "https://discord.com/api/v10"

def update_nickname(nickname: str, server_id: int):
    tries = 0
    while True:
        try:
            result = requests.patch(
                url = api_url + f"/guilds/{server_id}/members/@me",
                json = {"nick": nickname},
                headers = {"Authorization": token}
            )

            if result.status_code == 200:
                # success code
                return
            elif result.status_code == 401:
                # Unauthorized status code
                logging.error("Invalid token!")
                exit(1)
            elif result.status_code == 429:
                # rate limit status code
                rate_limit = result.headers["Retry-After"]

                logging.info(f"Rate limited by Discord. Waiting {rate_limit} seconds before trying again.")
                time.sleep(rate_limit)
            elif result.status_code == 403:
                logging.error(f"Dont have permission to change nickname in this server: {server_id}")
                exit(1)
        except Exception as e:
            logging.error(e)

            tries += 1

            if(tries >= 10):
                logging.info("Failed api call 10 times. QUITTING")
                exit(1)


def get_adv_progress(id: str) -> int:
    try:
        # grab any advancement file. non solo and non coop players wouldn't use this script
        filename = list(filter(lambda x: x.endswith(".json"), os.listdir(os.path.join(world_folder, "advancements"))))[0]
    except IndexError:
        logging.error("Empty advancements folder!")
        return 0 # no progress
    
    while True:
        try:
            with open(os.path.join(world_folder, "advancements", filename), "r") as f:
                j = json.load(f)
            break
        except IOError:
            # couldn't open file = its open by minecraft (autosave is happenning)
            logging.warning("Couldn't open advancement file, trying again in 3 seconds...")
            time.sleep(3)

    return len(j[id]["criteria"].keys())


def main():
    last_username = None

    while True:
        nick = get_nickname()

        if(last_username != nick):
            for server in servers:
                update_nickname(get_nickname(), server)
            last_username = nick
        
            logging.info("Updated your nickname, sleeping...")
        else:
            logging.info("Didn't change the nickname, sleeping...")

        time.sleep(delay)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye! Have a great day!!!")

