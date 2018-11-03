import config
import json

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

        # Use the thumb from the match article if available
        thumbnail = None
        if 'matchWrapArticle' in match:
            thumbnail = match['matchWrapArticle'].get('image')

        for ls in live_streams:
            # Only consider streams available in AU
            if 'AU' in [c['countryName'] for c in ls['streamCountriesList']]:
                name = "%s: %s v %s" % (match['series']['name'],
                                        match['homeTeam']['shortName'],
                                        match['awayTeam']['shortName'])
                video_list.append({
                    'video_id': ls['id'],
                    'name': name,
                    'thumbnail': thumbnail or ls.get('thumbnailUrl')
                })

    return video_list


def get_videos():
    video_list = []
    data = fetch_url(config.VIDEOS_URL)
    try:
        video_data = json.loads(data)
    except ValueError:
        utils.log('Failed to load JSON. Data is: {0}'.format(data))
        raise Exception('Failed to retrieve video data. Service may be '
                        'currently unavailable.')

    for video in video_data['videos']:
        video_list.append({
            'video_id': video['videoId'],
            'name': video['title'],
            'description': video['summary'],
            'thumbnail': video['thumbnailUrl'],
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

    stream_url = None
    for s in video_data['sources']:
        if 'src' in s and '.m3u8' in s['src']:
            stream_url = s['src']

    stream = {
        'url': stream_url,
        'name': video_data['name'],
    }
    return stream
