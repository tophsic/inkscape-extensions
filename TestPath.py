#!/usr/bin/env python

import path
import unittest
import sys

class TestPath(unittest.TestCase):

    def setUp(self):
        self.d = 'm 40,10 c -1,0 -3,1 -3,3 z'

    def test_parseRelativePath(self):
        p = path.Path(self.d, False)

        expected = [
                ['m', [40,10]],
                ['c', [-1,0,-3,1,-3,3]],
                ['z', []]
        ]

        self.assertEqual(expected, p.p)

    def test_FormatRelativePath(self):
        p = path.Path(self.d, False)

        expected = 'm40.0 10.0c-1.0 0.0 -3.0 1.0 -3.0 3.0z'

        self.assertEqual(expected, p.formatPath())

    def test_translatePointRelatively(self):

        p = path.Path(self.d, False)

        expected = 'm50.0 10.0'

        self.assertEqual(expected, p.translatePoint(0, 10, 0))

        expected = 'm50.0 10.0c-1.0 0.0 -3.0 1.0 -3.0 3.0z'

        self.assertEqual(expected, p.formatPath())


if __name__ == '__main__':
        unittest.main()
