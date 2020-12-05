import comm
import sys
import xbmcgui
import xbmcplugin

from aussieaddonscommon import utils


def make_list():
    try:
        videos = comm.get_videos()

        if len(videos) == 0:
            utils.dialog_message(['No videos found.',
                                  'Please try again later.'])
        else:
            for video in videos:
                url = "{0}?video_id={1}".format(sys.argv[0], video['video_id'])
                listitem = xbmcgui.ListItem(video['name'])
                listitem.setArt({'icon': video['thumbnail'],
                                 'thumb': video['thumbnail']})
                listitem.setProperty('IsPlayable', 'true')
                listitem.setInfo('video', {'plot': video['name']})

                # add the item to the media list
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                            url=url,
                                            listitem=listitem,
                                            isFolder=False,
                                            totalItems=len(videos))

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
    except Exception:
        utils.handle_error('Unable build video list')
