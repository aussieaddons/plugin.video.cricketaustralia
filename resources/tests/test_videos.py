from __future__ import absolute_import, unicode_literals

import importlib
import io
import os

try:
    import mock
except ImportError:
    import unittest.mock as mock

import responses

import testtools

import resources.lib.config as config
from resources.tests.fakes import fakes


class VideosTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/video.json'), 'rb') as f:
            self.VIDEO_JSON = io.BytesIO(f.read()).read()

    def setUp(self):
        super(VideosTests, self).setUp()
        self.mock_plugin = fakes.FakePlugin()
        self.patcher = mock.patch.dict('sys.modules',
                                       xbmcplugin=self.mock_plugin)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        global videos
        videos = importlib.import_module('resources.lib.videos')

    def tearDown(self):
        super(VideosTests, self).tearDown()
        self.patcher.stop()
        self.mock_plugin = None

    @mock.patch('xbmcgui.ListItem', fakes.FakeListItem)
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?category=Latest%20News',
                             'resume:false'])
    @responses.activate
    def test_make_list(self):
        responses.add('GET', config.VIDEOS_URL, body=self.VIDEO_JSON)
        videos.make_list()
        self.assertEqual(50, len(self.mock_plugin.directory))
        self.assertEqual(
            "The story behind India fan's special SCG proposal",
            self.mock_plugin.directory[0].get('listitem').getLabel())
