import comm
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils




def play(params):
    try:
        import drmhelper
        if not drmhelper.check_inputstream(drm=False):
            return
    except ImportError:
        utils.log("Failed to import drmhelper")
        utils.dialog_message(
            'DRM Helper is needed for inputstream.adaptive '
            'playback. For more information, please visit: '
            'http://aussieaddons.com/drm')
        return

    try:
        pluginhandle = int(sys.argv[1])
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
