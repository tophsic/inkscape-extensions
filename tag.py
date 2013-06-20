#!/usr/bin/env python

import inkex
import gettext
import sys
import functions
import path

_ = gettext.gettext

class Tag(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--text",
                                action="store", type="string",
                                dest="text",
                                help="")
    def effect(self):
        dimensions = functions.getDimensions(sys.argv[-1], 'text')
        x = dimensions[1]
        y = dimensions[2]
        width = dimensions[3]
        height = dimensions[4]

        roundShape = self.document.xpath('//*[@id="tag1"]',namespaces=inkex.NSS)[0]
        tagShape = self.document.xpath('//*[@id="tag2"]',namespaces=inkex.NSS)[0]

        d = roundShape.get('d')
        currentPath = path.Path(d, False)
        move = float(x) + float(width) 
        x_1_start = currentPath.getXPoint(0)
        test = currentPath.movePoint(0, move + 5, None)
        x_1_end = currentPath.getXPoint(0)
        roundShape.set('d', currentPath.formatPath())

        d = tagShape.get('d')
        currentPath = path.Path(d)
        move = float(x) + float(width) 
        #tagShape.set('d', currentPath.formatPath())
        x_2_start = currentPath.getXPoint(0)
        diff = x_2_start - x_1_start
        currentPath.movePoint(0, x_1_end + diff, None)
        x_2_start = currentPath.getXPoint(1)
        diff = x_2_start - x_1_start
        currentPath.movePoint(1, x_1_end + diff, None)
        x_2_start = currentPath.getXPoint(2)
        diff = x_2_start - x_1_start
        currentPath.movePoint(2, x_1_end + diff, None)
        tagShape.set('d', currentPath.formatPath())

if __name__ == '__main__':
        e = Tag()
        e.affect()

