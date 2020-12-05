from __future__ import absolute_import, unicode_literals

import io
import os
import re

import responses

import testtools

import resources.lib.comm as comm
import resources.lib.config as config


class CommTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/bc.json'), 'rb') as f:
            self.BRIGHTCOVE_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/stream.json'), 'rb') as f:
            self.STREAM_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/video.json'), 'rb') as f:
            self.VIDEO_JSON = io.BytesIO(f.read()).read()

    @responses.activate
    def test_get_matches(self):
        responses.add(responses.GET, config.MATCHES_URL,
                      body=self.STREAM_JSON, status=200)
        observed = comm.get_matches()
        self.assertEqual('Marsh Sheffield Shield 2020-21: SA v WA',
                         observed[0].get('name'))

    @responses.activate
    def test_get_videos(self):
        responses.add(responses.GET, config.VIDEOS_URL,
                      body=self.VIDEO_JSON, status=200)
        observed = comm.get_videos()
        self.assertEqual("The story behind India fan's special SCG proposal",
                         observed[0].get('name'))

    @responses.activate
    def test_get_stream(self):
        responses.add('GET', re.compile(config.MATCH_STREAM_URL),
                      body=self.BRIGHTCOVE_JSON)
        observed = comm.get_stream('1234')
        expect = {'url': 'https://foo.bar/master.m3u8',
                  'name': "The story behind India fan's special SCG proposal"}
        self.assertEqual(expect, observed)
