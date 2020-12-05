import sys

from aussieaddonscommon import utils

import resources.lib.index as index
import resources.lib.matches as matches
import resources.lib.play as play
import resources.lib.videos as videos

# Print our platform/version debugging information
utils.log_kodi_platform_version()


def main():
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


if __name__ == "__main__":
    main()
