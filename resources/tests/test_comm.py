from __future__ import absolute_import, unicode_literals

import io
import json
import os

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
# from resources.tests.fakes import fakes


class CommTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/stream.json'), 'rb') as f:
            self.STREAM_JSON = io.BytesIO(f.read()).read()

    @responses.activate
    def test_get_matches(self):
        responses.add(responses.GET, config.MATCHES_URL,
                      body=self.STREAM_JSON, status=200)
        observed = comm.get_matches()
        self.assertEqual('Marsh Sheffield Shield 2020-21: SA v WA',
                         observed[0].get('name'))
