import os
import sys
import urllib
import xbmcaddon
import xbmc
import xbmcgui
import xbmcplugin
import requests
from urllib.parse import parse_qs, urlencode


def build_url(query):
    base_url = sys.argv[0]
    dialog = xbmcgui.Dialog()
    dialog.notification('RetroWave Player', 'Base Url: '+base_url, xbmcgui.NOTIFICATION_INFO, 5000)
    return base_url + '?' + urlencode(query)


def getMusicList():
    song_list = []
    URL = "http://retrowave.ru/api/v1/tracks"
    PARAMS = {'cursor': 1, 'limit': 3}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    for song in data['body']['tracks']:
        li = xbmcgui.ListItem(label=song['title'])
        li.setArt({'thumb': 'http://retrowave.ru/' + song['artworkUrl'], 'fanart': 'http://retrowave.ru/' + song['artworkUrl']})
        url = build_url({'mode': 'stream', 'url': 'http://retrowave.ru' + song['streamUrl'], 'title': song['title'], 'artwork': 'http://retrowave.ru/' + song['artworkUrl']})
        song_list.append((url, li, False))

    xbmcplugin.addDirectoryItems(addon_handle, song_list, len(song_list))
    xbmcplugin.setContent(addon_handle, 'songs')
    xbmcplugin.endOfDirectory(addon_handle)

def play_song(url,title, artwork):
    play_item = xbmcgui.ListItem(path=url,label=title)
    play_item.setArt({'thumb': artwork, 'fanart': artwork})

    dialog = xbmcgui.Dialog()
    # dialog.notification('RetroWave Player', 'Mode: '+url, xbmcgui.NOTIFICATION_INFO, 5000)
    # xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
    xbmc.Player().play(item=url, listitem=play_item)

def main():
    args = parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    
    if mode is None:
        getMusicList()
    elif mode[0] == 'stream':
        dialog = xbmcgui.Dialog()
        dialog.notification('RetroWave Player', 'Mode: '+args['title'][0], xbmcgui.NOTIFICATION_INFO, 5000)
        play_song(args['url'][0], args['title'][0], args['artwork'][0])

if __name__ == '__main__':
    addon_handle = int(sys.argv[1])
    main()
