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

from resources.tests.fakes import fakes


class AddonTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/bc.json'), 'rb') as f:
            self.BRIGHTCOVE_JSON = io.BytesIO(f.read()).read()

    def setUp(self):
        super(AddonTests, self).setUp()
        self.mock_plugin = fakes.FakePlugin()
        self.patcher = mock.patch.dict('sys.modules',
                                       xbmcplugin=self.mock_plugin)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        global addon
        addon = importlib.import_module('addon')

    def tearDown(self):
        super(AddonTests, self).tearDown()
        self.patcher.stop()
        self.mock_plugin = None

    @mock.patch('resources.lib.play.play')
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?video_id=1234',
                             'resume:false'])
    @responses.activate
    def test_addon_play(self, mock_play):
        addon.main()
        mock_play.assert_called_with({'video_id': '1234'})

    @mock.patch('resources.lib.videos.make_list')
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?category=Latest%20News',
                             'resume:false'])
    @responses.activate
    def test_addon_videos_list(self, mock_list):
        addon.main()
        mock_list.assert_called_once()

    @mock.patch('resources.lib.matches.make_list')
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?category=Live%20Matches',
                             'resume:false'])
    @responses.activate
    def test_addon_matches_list(self, mock_list):
        addon.main()
        mock_list.assert_called_once()

    @mock.patch('resources.lib.index.make_list')
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '',
                             'resume:false'])
    @responses.activate
    def test_addon_index_list(self, mock_list):
        addon.main()
        mock_list.assert_called_once()
