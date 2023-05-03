# Plex-Now-Playing
This is a python script that when running listens for the currently playing song and retrieves the title, artist, and album art, and saves it into the current directory (configurable)

Requires Plex Media Server to be runnning. Doesn't matter if it's running on this machine or another.

You need to get your Plex Token. Instructions are here: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

You also need the URL of your Plex Server and the name of your Plex Client.

Installing Plex-Now-Playing

`pip install -r requirements.txt`

Then open plexamp.py and add the required things like your Plex Token, the URL of your Plex Server, and the name of your Plex Client.

Running Plex-Now-Playing

`python plexamp.py`

Example of integrating it within OBS:

https://user-images.githubusercontent.com/24556317/235816006-61a5f598-8711-43a2-a3d1-f3ca41bda650.mp4
