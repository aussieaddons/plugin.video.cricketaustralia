import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils

import resources.lib.config as config


def make_list():
    try:
        for category in config.CATEGORIES:
            url = "{0}?category={1}".format(sys.argv[0], category)
            listitem = xbmcgui.ListItem(category)

            # add the item to the media list
            ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                             url=url,
                                             listitem=listitem,
                                             isFolder=True,
                                             totalItems=len(config.CATEGORIES))

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=ok)
    except Exception:
        raise
        utils.handle_error('Unable build video category list')
