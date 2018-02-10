import comm
import config
import os
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
        item = xbmcgui.ListItem(label=stream['name'],
                                path=stream['url'])
        item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        item.setMimeType('application/vnd.apple.mpegurl')
        item.setContentLookup(False)
        xbmcplugin.setResolvedUrl(pluginhandle, True, listitem=item)
    except Exception:
        utils.handle_error('Unable to play video')

