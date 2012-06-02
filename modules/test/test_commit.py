"""
test_commit.py - tests for the what the commit module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import unittest
from mock import MagicMock
from modules.commit import commit


class TestCommit(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_commit(self):
        commit(self.phenny, None)
        assert self.phenny.reply.called is True
