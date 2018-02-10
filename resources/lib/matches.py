import comm
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils

def make_list():
    try:
        matches = comm.get_matches()
        for match in matches:
            url = "%s?video_id=%s" % (sys.argv[0], match['video_id'])
            listitem = xbmcgui.ListItem(match['name'])

            # add the item to the media list
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                             url=url,
                                             listitem=listitem,
                                             isFolder=False,
                                             totalItems=len(matches))

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
    except Exception:
        utils.handle_error('Unable build match list')
