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

        # TODO(andy): Fix strm file hack
        strm = os.path.join(utils.get_file_dir(), 'stream.strm')
        with open(strm, 'w') as f:
            f.write('#KODIPROP:inputstreamaddon=inputstream.adaptive\n'
                    '#KODIPROP:inputstream.adaptive.manifest_type=hls\n'
                    '{0}'.format(stream['url']))

        item = xbmcgui.ListItem(path=stream['url'])
        xbmc.Player().play(item)

        #item = xbmcgui.ListItem(path=stream['url'])
        #item.setProperty('inputstreamaddon', 'inputstream.adaptive')
        #item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        #item.setMimeType('application/vnd.apple.mpegurl')
        #item.setContentLookup(False)
        #xbmcplugin.setResolvedUrl(pluginhandle, True, item=item)
    except Exception:
        utils.handle_error('Unable to play video')

