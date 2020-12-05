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


class MatchesTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/stream.json'), 'rb') as f:
            self.STREAM_JSON = io.BytesIO(f.read()).read()

    def setUp(self):
        super(MatchesTests, self).setUp()
        self.mock_plugin = fakes.FakePlugin()
        self.patcher = mock.patch.dict('sys.modules',
                                       xbmcplugin=self.mock_plugin)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        global matches
        matches = importlib.import_module('resources.lib.matches')

    def tearDown(self):
        super(MatchesTests, self).tearDown()
        self.patcher.stop()
        self.mock_plugin = None

    @mock.patch('xbmcgui.ListItem', fakes.FakeListItem)
    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '?category=Live%20Matches',
                             'resume:false'])
    @responses.activate
    def test_make_list(self):
        responses.add('GET', config.MATCHES_URL, body=self.STREAM_JSON)
        matches.make_list()
        self.assertEqual(2, len(self.mock_plugin.directory))
        self.assertEqual(
            'Marsh Sheffield Shield 2020-21: SA v WA',
            self.mock_plugin.directory[0].get('listitem').getLabel())
