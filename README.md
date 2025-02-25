# umm... is this thing on?
This python program will update your nickname on a server of your choice to show your advancement progress for BAC

and yes, you will need a token

# Usage
1. Install [Python](https://www.python.org/downloads/) if you dont have it yet
2. Download this repo as zip (and unzip) OR download main.py file
3. Modify some values in main.py file:
- delay - cooldown between each nickname update
- servers - a list of server ids of all servers where you want your nickname to be changed
- get_nickname - this is what your nickname will look like (except get_adv_progress(...) will be replaced with your adv progress)<br>
you can use multiple get_adv_progress! all of them must be inside {} (dont put two of them in one {}, separate them)
- token - your discord token.
- world_folder - full path to your world folder. DO NOT use backslash (\). either use normal slash / or have all double backslashes \\
4. you can now run this python program. `python main.py` in console will work. for those who dont even know what console is: double clicking might work, or google how to open console
5. `Ctrl + c` when you want to stop the program.

# How to find Discord token?
- Open discord in web browser or desktop client.
- Open dev tools (ctrl + shift + i)
- open network tab
- Open any channel in any server.
- Find something like `messages?limit=50` request.
- Click it and find Authorization in Request Headers
- Copy this token and use it.

# IF YOU LEAK YOUR TOKEN OR SOMETHING IMMEDIATELY LOG OUT OF THAT BROWSER/APP WHERE YOU GOT YOUR TOKEN FROM
