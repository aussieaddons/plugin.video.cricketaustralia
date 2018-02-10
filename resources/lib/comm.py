import config
import json
import xbmcaddon

from aussieaddonscommon import session
from aussieaddonscommon import utils


def fetch_url(url, headers=None):
    """Simple function that fetches a URL using requests."""
    with session.Session() as sess:
        if headers:
            sess.headers.update(headers)

        request = sess.get(url)
        try:
            request.raise_for_status()
        except Exception as e:
            # Just re-raise for now
            raise e
    return request.text


def get_matches():
    video_list = []
    data = fetch_url(config.MATCHES_URL)
    try:
        video_data = json.loads(data)
    except ValueError:
        utils.log('Failed to load JSON. Data is: {0}'.format(data))
        raise Exception('Failed to retrieve video data. Service may be '
                        'currently unavailable.')

    for match in video_data['matchList']['matches']:
        live_streams = match['liveStreams']
        for ls in live_streams:
            if 'AU' in [c['countryName'] for c in ls['streamCountriesList']]:
                video_list.append({
                    'video_id': ls['id'],
                    'name': "%s: %s v %s" % (
                        match['name'],
                        match['homeTeam']['name'],
                        match['awayTeam']['name'],
                    )
                })

    return video_list


def get_stream(video_id):
    headers = {
        'Accept': 'application/json;pk=%s' % config.BRIGHTCOVE_PK,
        'Origin': 'http://live.cricket.com.au',
    }
    url = config.MATCH_STREAM_URL + video_id
    data = fetch_url(url, headers=headers)
    try:
        video_data = json.loads(data)
    except ValueError:
        utils.log('Failed to load JSON. Data is: {0}'.format(data))
        raise Exception('Failed to retrieve video data. Service may be '
                        'currently unavailable.')

    stream = {
        'url': video_data['sources'][0]['src'],
        'name': video_data['name'],
    }   
    return stream
