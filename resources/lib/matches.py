import comm
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils


def make_list():
    try:
        matches = comm.get_matches()

        if len(matches) == 0:
            utils.dialog_message(['No matches are currently being played.',
                                  'Please try again later.'])
        else:
            for match in matches:
                url = "%s?video_id=%s" % (sys.argv[0], match['video_id'])
                listitem = xbmcgui.ListItem(match['name'],
                                            iconImage=match['thumbnail'],
                                            thumbnailImage=match['thumbnail'])
                listitem.setProperty('IsPlayable', 'true')
                listitem.setInfo('video', {'plot': match['name']})

                # add the item to the media list
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                            url=url,
                                            listitem=listitem,
                                            isFolder=False,
                                            totalItems=len(matches))

        xbmcplugin.endOfDirectory(
            handle=int(sys.argv[1]), cacheToDisc=False)
    except Exception:
        utils.handle_error('Unable build match list')
