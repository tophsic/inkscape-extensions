#!/usr/bin/env python

import inkex
import gettext
import sys
import functions

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

                tagEls = self.document.xpath('//*[@id="tag"]/*/svg:path',namespaces=inkex.NSS)
                #tspan = self.document.xpath('//*[@id="text"]/svg:tspan',namespaces=inkex.NSS)[0]
                #tspan.text = self.options.text
                
                roundShape = tagEls[1]
                inkex.debug(roundShape.keys())
                inkex.debug(roundShape.get('d'))

if __name__ == '__main__':
        e = Tag()
        e.affect()

