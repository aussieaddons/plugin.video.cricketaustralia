from __future__ import absolute_import, unicode_literals

import importlib
import io
import os
import re

try:
    import mock
except ImportError:
    import unittest.mock as mock

import responses

import testtools

import resources.lib.config as config
from resources.tests.fakes import fakes


class PlayTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/bc.json'), 'rb') as f:
            self.BRIGHTCOVE_JSON = io.BytesIO(f.read()).read()

    def setUp(self):
        super(PlayTests, self).setUp()
        self.mock_plugin = fakes.FakePlugin()
        self.patcher = mock.patch.dict('sys.modules',
                                       xbmcplugin=self.mock_plugin)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        global play
        play = importlib.import_module('resources.lib.play')

    def tearDown(self):
        super(PlayTests, self).tearDown()
        self.patcher.stop()
        self.mock_plugin = None

    @mock.patch('drmhelper.check_inputstream')
    @mock.patch('xbmcgui.ListItem', fakes.FakeListItem)
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?video_id=1234',
                             'resume:false'])
    @responses.activate
    def test_play(self, mock_drmhelper):
        mock_drmhelper.return_value = True
        responses.add('GET', re.compile(config.MATCH_STREAM_URL),
                      body=self.BRIGHTCOVE_JSON)
        params = {'video_id': '1234'}
        play.play(params)
        self.assertEqual(
            "The story behind India fan's special SCG proposal",
            self.mock_plugin.resolved[2].getLabel())
        self.assertEqual('https://foo.bar/master.m3u8',
                         self.mock_plugin.resolved[2].getPath())
