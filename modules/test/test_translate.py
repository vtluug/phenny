"""
test_translate.py - tests for the translation module
author: mutantmonkey <mutantmonkey@mutantmonkey.in>
"""

import re
import unittest
from mock import MagicMock, Mock
from modules.translate import translate, tr, tr2, mangle


class TestTranslation(unittest.TestCase):
    def setUp(self):
        self.phenny = MagicMock()

    def test_translate(self):
        out = translate("plomo o plata", input='es')
        self.assertEqual(('lead or silver', 'es'), out)

    def test_tr(self):
        input = Mock(groups=lambda: ('fr', 'en', 'mon chien'))
        tr(self.phenny, input)

        self.assertIn("my dog", self.phenny.reply.call_args[0][0])

    def test_tr2(self):
        input = Mock(group=lambda x: 'Estoy bien')
        tr2(self.phenny, input)

        self.assertIn("'m fine", self.phenny.reply.call_args[0][0])

    def test_translate_bracketnull(self):
        input = Mock(group=lambda x: 'Moja je lebdjelica puna jegulja')
        tr2(self.phenny, input)

        self.assertIn("My hovercraft is full of eels",
                      self.phenny.reply.call_args[0][0])

    def test_mangle(self):
        input = Mock(group=lambda x: 'Mangle this phrase!')
        mangle(self.phenny, input)

        self.phenny.reply.assert_not_called_with('ERRORS SRY')
