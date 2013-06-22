#!/usr/bin/env python

import inkex
import sys
import functions
import re

class Document(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        dimensions = functions.getDimensions(sys.argv[-1], 'tag2')
        x = float(dimensions[1])
        widthTo = str(x + float(dimensions[3]) + x)

        document = self.document.getroot()
        widthFrom = document.get('width')
        viewBox = document.get('viewBox').split(' ')
        viewBox[2] = widthTo

        document.set('viewBox', ' '.join(viewBox))
        document.set('width', widthTo)


if __name__ == '__main__':
        e = Document()
        e.affect()

