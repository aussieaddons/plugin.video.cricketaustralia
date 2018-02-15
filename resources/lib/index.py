import config
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils


def make_list():
    try:
        for category in config.CATEGORIES:
            url = "%s?category=%s" % (sys.argv[0], category)
            listitem = xbmcgui.ListItem(category)

            # add the item to the media list
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                             url=url,
                                             listitem=listitem,
                                             isFolder=True,
                                             totalItems=len(config.CATEGORIES))

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=ok)
    except Exception:
        utils.handle_error('Unable build video category list')
