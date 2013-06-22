#!/usr/bin/env python

import inkex
import sys
import functions
import path

class Tag(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

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
        tagShape.set('d', currentPath.formatPath())

        points = [0, 1, 2, 9, 10, 11, 12, 14, 15, 16, 23, 24, 25, 26]
	    
        for point in points:
                x_2_start = currentPath.getXPoint(point)
                diff = x_2_start - x_1_start
                currentPath.movePoint(point, x_1_end + diff, None)

        tagShape.set('d', currentPath.formatPath())

if __name__ == '__main__':
        e = Tag()
        e.affect()

