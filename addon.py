import os
import sys
import xbmcaddon

from aussieaddonscommon import utils

# Add our resources/lib to the python path
addon_dir = xbmcaddon.Addon().getAddonInfo('path')
sys.path.insert(0, os.path.join(addon_dir, 'resources', 'lib'))

import matches  # noqa: E402
import play  # noqa: E402

# Print our platform/version debugging information
utils.log_kodi_platform_version()

if __name__ == "__main__":

    params_str = sys.argv[2]
    params = utils.get_url(params_str)
    utils.log('Loading with params: {0}'.format(params))

    if len(params) == 0:
        matches.make_list()
    elif 'video_id' in params:
        play.play(params)
