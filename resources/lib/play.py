import comm
import config
import sys
import xbmc
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils

pluginhandle = int(sys.argv[1])

def play(params):
    try:
        success = True
        stream = comm.get_stream(params['video_id'])

        utils.log('Attempting to play: {0} {1}'.format(stream['name'],
                                                       stream['url']))

        listitem = xbmcgui.ListItem(path=stream['url'])
        listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
        listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        listitem.setMimeType('application/vnd.apple.mpegurl')
        listitem.setContentLookup(False)

        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem=listitem)
    except Exception:
        utils.handle_error('Unable to play video')

