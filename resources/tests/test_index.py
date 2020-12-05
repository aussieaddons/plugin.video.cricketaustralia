from __future__ import absolute_import, unicode_literals

import importlib
import io
import os
from builtins import str

try:
    import mock
except ImportError:
    import unittest.mock as mock

from future.moves.urllib.parse import quote_plus

import requests

import responses

import testtools

import resources.lib.comm as comm
import resources.lib.config as config
from resources.tests.fakes import fakes


class IndexTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/video.json'), 'rb') as f:
            self.VIDEO_JSON = io.BytesIO(f.read()).read()

    def setUp(self):
        super(IndexTests, self).setUp()
        self.mock_plugin = fakes.FakePlugin()
        self.patcher = mock.patch.dict('sys.modules',
                                       xbmcplugin=self.mock_plugin)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        global index
        index = importlib.import_module('resources.lib.index')

    def tearDown(self):
        super(IndexTests, self).tearDown()
        self.patcher.stop()
        self.mock_plugin = None

    @mock.patch('sys.argv', ['plugin://plugin.video.cricketaustralia/', '5',
                             '',
                             'resume:false'])
    def test_make_list(self):
        index.make_list()
        self.assertEqual(2, len(self.mock_plugin.directory))