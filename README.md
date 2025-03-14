# umm... is this thing on?
This python program will update your nickname on a server of your choice to show your advancement progress for BAC

and yes, you will need a token

# Usage
1. Install [Python](https://www.python.org/downloads/) if you dont have it yet
2. Download this repo as zip (and unzip) OR `git clone` it
3. install missing libraries: `pip install -r requirements.txt`
4. Run `main.py` for the first time: `python3 main.py`
5. Set up `config.json` after generating
   - `delay` - cooldown between each nickname update
   - `servers` a list of server ids of all servers where you want your nickname to be changed
   - `world_folder`: full path to your world folder. DO NOT use backslash (\). either use normal slash / or have all double backslashes \\
   - `nickname`: your nickname without "[progress/total]" etc.
   - `total_advancements`: total amount of advancement (1152 is for BACAP 1.18.1)
   - `progress_pattern` REGEX pattern that will be used to update your nickname, default one is `<NAME> [<COMPLETED_ADV>/<TOTAL_ADV>]`, it will look something like this: `SuperName [611/1152]`
6. Set up `TOKEN` in the `.env` file
7. Run `main.py` again, if you do everything correctly, it will work
8. `Ctrl + c` when you want to stop the program.

# How to find Discord token?
1. Open discord in web browser or desktop client.
2. Open dev tools (ctrl + shift + i)
3. open `Network` tab
4. Find `science` request
5. Find `Authorization` in the `Headers` section, this will be your token
6. Copy this token and use it.

# IF YOU LEAK YOUR TOKEN OR SOMETHING, IMMEDIATELY LOG OUT OF THAT BROWSER/APP WHERE YOU GOT YOUR TOKEN FROM
