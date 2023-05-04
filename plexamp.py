import asyncio
import os
import requests
from plexapi.server import PlexServer
from plexwebsocket import PlexWebsocket, SIGNAL_CONNECTION_STATE
from plexapi.myplex import MyPlexAccount

# Change these variables
plex_server_url = 'http://localhost:32400' # Change this to your Plex server IP address
plex_token = 'xdd' # Change this to your Plex token https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
client_name = 'My-PC-Example' # Change this to whatever client you want to get the information from
directory = os.getcwd() # Change this to whatever directory you want the information to be saved to ex: "C:/mydir/" make sure to include the trailing slash
# End of variables to change

baseurl = plex_server_url
token = plex_token
plex = PlexServer(baseurl, token)
clientCheck = True
while clientCheck == True: # This is to prevent the script from crashing if the client is not found
    try:
        client = plex.client(client_name)
        clientCheck = False
    except:
        print("Client not found")
        clientCheck = True
machineID = client.machineIdentifier
mydir = directory

def save_album_art(item):
    """
    Saves the album art of the provided media item to album.png file.
    """
    album_art_url = item.parentThumb
    if album_art_url is None:
        album_art_url = item.grandparentThumb
    if album_art_url:
        #print(baseurl + album_art_url)
        album_art = requests.get(baseurl + album_art_url + f'?X-Plex-Token={token}').content
        with open (f"{mydir}album_art.txt", "w+") as f:
            f.write(baseurl + album_art_url + f'?X-Plex-Token={token}')
        with open(f"{mydir}album.png", "wb") as f:
            f.write(album_art)
    else:
        print("No album art found")

def print_info(msgtype, data, error):
    """
    Prints the artist and song title of the currently playing song.
    """
    if msgtype == SIGNAL_CONNECTION_STATE:
        print(f"State: {data} / Error: {error}")
    else:
        if data['PlaySessionStateNotification'][0]['clientIdentifier'] != machineID: # This is to prevent the script from running for other clients
            return
        else:
            if data['type'] == 'playing': # This is to prevent the script from running when the song is paused
                try:
                    with open (f"{mydir}rating_key.txt", "r") as f: # This is to prevent the script from running multiple times for the same song
                        last_rating_key = f.read()
                except:
                    last_rating_key = None
                if last_rating_key == data['PlaySessionStateNotification'][0]['ratingKey']:
                    return
                else:
                    rating_key = data['PlaySessionStateNotification'][0]['ratingKey'] # This is the unique ID of the song
                    with open (f"{mydir}rating_key.txt", "w", encoding='utf-8') as f:
                        f.write(rating_key)
                    #print(f"Rating key: {rating_key}")
                    item_path = f"/library/metadata/{rating_key}" # This is the path to the song
                    item = plex.fetchItem(item_path, cls=None, container_start=None, container_size=None) # This gets the song information
                    grandparent_title = item.grandparentTitle # This is the artist
                    title = item.title # This is the song title
                    # Print the artist and song title
                    try:
                        print(f"{grandparent_title} - {title}")
                    except:
                        print(f"New song playing but cannot be displayed") # This is to prevent the script from crashing if the song title cannot be displayed due to an encoding issue on Windows
                    with open (f"{mydir}artist.txt", "w", encoding='utf-8') as f: # This is to save the artist to a text file
                        f.write(grandparent_title)
                    with open (f"{mydir}song.txt", "w", encoding='utf-8') as f: # This is to save the song title to a text file
                        f.write(title)
                    # Save the album art to an image file
                    save_album_art(item) # This is to save the album art to an image file
                
async def main():
    ws = PlexWebsocket(plex, print_info, subscriptions=["playing"])
    await ws.listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
