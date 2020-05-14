#!/usr/bin/env python3

import unittest
import install


class RunCommandTestCase(unittest.TestCase):

    def test_correct_command(self):
        params = ['ls', '-l']
        desired = 'command \'ls -l\' executed succesfully'
        self.assertEqual(install.run_command(params), desired)
