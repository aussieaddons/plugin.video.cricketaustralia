import os
import sys
import xbmcaddon
import xbmcgui

from aussieaddonscommon import utils

# Add our resources/lib to the python path
addon_dir = xbmcaddon.Addon().getAddonInfo('path')
sys.path.insert(0, os.path.join(addon_dir, 'resources', 'lib'))

import index  # noqa: E402
import matches  # noqa: E402
import play  # noqa: E402
import videos  # noqa: E402

# Print our platform/version debugging information
utils.log_kodi_platform_version()

if __name__ == "__main__":

    params_str = sys.argv[2]
    params = utils.get_url(params_str)
    utils.log('Loading with params: {0}'.format(params))

    if len(params) == 0:
        index.make_list()
    elif 'category' in params:
        if params['category'] == 'Live Matches':
            matches.make_list()
        elif params['category'] == 'Latest News':
            videos.make_list()
        else:
            index.make_list()
    elif 'video_id' in params:
        play.play(params)
    elif 'action' in params:
        if params['action'] == 'sendreport':
            utils.user_report()
        elif params['action'] == 'update_ia':
            try:
                import drmhelper
                addon = drmhelper.get_addon(drm=False)
                if not drmhelper.is_ia_current(addon, latest=True):
                    if xbmcgui.Dialog().yesno(
                        'Upgrade?', ('Newer version of inputstream.adaptive '
                                     'available ({0}) - would you like to '
                                     'upgrade to this version?'.format(
                                        drmhelper.get_latest_ia_ver()))):
                        drmhelper.get_ia_direct(update=True, drm=False)
                else:
                    ver = addon.getAddonInfo('version')
                    utils.dialog_message('Up to date: Inputstream.adaptive '
                                         'version {0} installed and enabled.'
                                         ''.format(ver))
            except ImportError:
                utils.log("Failed to import drmhelper")
                utils.dialog_message('DRM Helper is needed for this function. '
                                     'For more information, please visit: '
                                     'http://aussieaddons.com/drm')
