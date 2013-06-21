#!/usr/bin/env python

import re, math, sys

class Path():

    '''
    pathdefs = {commandfamily:
        [
        implicitnext,
        #params,
        [casts,cast,cast],
        [coord type,x,y,0]
        ]}
    '''
    pathdefs = {
        'M':['L', 2, [float, float], ['x','y']], 
        'L':['L', 2, [float, float], ['x','y']], 
        'H':['H', 1, [float], ['x']], 
        'V':['V', 1, [float], ['y']], 
        'C':['C', 6, [float, float, float, float, float, float], ['x','y','x','y','x','y']], 
        'S':['S', 4, [float, float, float, float], ['x','y','x','y']], 
        'Q':['Q', 4, [float, float, float, float], ['x','y','x','y']], 
        'T':['T', 2, [float, float], ['x','y']], 
        'A':['A', 7, [float, float, float, int, int, float, float], ['r','r','a',0,'s','x','y']], 
        'Z':['L', 0, [], []]
        }
    def __init__(self, d, absolute = True):
        self.absolute = absolute
        self.p = self.parsePath(d)

    def lexPath(self, d):
        """
        returns and iterator that breaks path data 
        identifies command and parameter tokens
        """
        offset = 0
        length = len(d)
        delim = re.compile(r'[ \t\r\n,]+')
        command = re.compile(r'[MLHVCSQTAZmlhvcsqtaz]')
        parameter = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')
        while 1:
            m = delim.match(d, offset)
            if m:
                offset = m.end()
            if offset >= length:
                break
            m = command.match(d, offset)
            if m:
                yield [d[offset:m.end()], True]
                offset = m.end()
                continue
            m = parameter.match(d, offset)
            if m:
                yield [d[offset:m.end()], False]
                offset = m.end()
                continue
            #TODO: create new exception
            raise Exception, 'Invalid path data!'

    def parsePath(self, d):
        """
        Parse SVG path and return an array of segments.
        Removes all shorthand notation.
        Converts coordinates to absolute... or not :P
        """
        retval = []
        lexer = self.lexPath(d)

        pen = (0.0,0.0)
        subPathStart = pen
        lastControl = pen
        lastCommand = ''
        
        while 1:
            try:
                token, isCommand = lexer.next()
            except StopIteration:
                break
            params = []
            needParam = True
            if isCommand:
                if not lastCommand and token.upper() != 'M':
                    raise Exception, 'Invalid path, must begin with moveto.'    
                else:                
                    command = token
            else:
                #command was omited
                #use last command's implicit next command
                needParam = False
                if lastCommand:
                    if lastCommand.isupper():
                        command = self.pathdefs[lastCommand][0]
                    else:
                        command = self.pathdefs[lastCommand.upper()][0].lower()
                else:
                    raise Exception, 'Invalid path, no initial command.'    
            numParams = self.pathdefs[command.upper()][1]
            while numParams > 0:
                if needParam:
                    try: 
                        token, isCommand = lexer.next()
                        if isCommand:
                            raise Exception, 'Invalid number of parameters'
                    except StopIteration:
                        raise Exception, 'Unexpected end of path'
                cast = self.pathdefs[command.upper()][2][-numParams]
                param = cast(token)
                if command.islower() and self.absolute is True:
                    if self.pathdefs[command.upper()][3][-numParams]=='x':
                        param += pen[0]
                    elif self.pathdefs[command.upper()][3][-numParams]=='y':
                        param += pen[1]
                params.append(param)
                needParam = True
                numParams -= 1
            if self.absolute is True:
                #segment is now absolute so
                outputCommand = command.upper()
            else:
                outputCommand = command
        
            #Flesh out shortcut notation    
            if outputCommand in ('H','V'):
                if outputCommand == 'H':
                    params.append(pen[1])
                if outputCommand == 'V':
                    params.insert(0,pen[0])
                outputCommand = 'L'
            if outputCommand in ('S','T'):
                params.insert(0,pen[1]+(pen[1]-lastControl[1]))
                params.insert(0,pen[0]+(pen[0]-lastControl[0]))
                if outputCommand == 'S':
                    outputCommand = 'C'
                if outputCommand == 'T':
                    outputCommand = 'Q'

            #current values become "last" values
            if outputCommand == 'M':
                subPathStart = tuple(params[0:2])
                pen = subPathStart
            if outputCommand == 'Z':
                pen = subPathStart
            else:
                pen = tuple(params[-2:])

            if outputCommand in ('Q','C'):
                lastControl = tuple(params[-4:-2])
            else:
                lastControl = pen
            lastCommand = command

            retval.append([outputCommand,params])
        return retval

    def formatPath(self, a = None):
        p = self.p

        if a is not None:
            p = a

        """Format SVG path data from an array"""
        return "".join([cmd + " ".join([str(p) for p in params]) for cmd, params in p])

    def movePoint(self, index, x, y):
        pt = self.p[index]
        command = pt[0].upper()

        if self.pathdefs.has_key(command) is False:
            raise Exception, 'Invalid command'

        if command in ['M', 'L']:
            if x is not None:
                pt[1][0] = x
            if y is not None:
                pt[1][1] = y
        elif command == 'C':
            if x is not None:
		pt[1][0] = x + (pt[1][0] - pt[1][4])
		pt[1][2] = x + (pt[1][2] - pt[1][4])
                pt[1][4] = x
            if y is not None:
                pt[1][5] = y

        return self.formatPath([pt])

    def pointToAbsolute(self, index):
        pt = self.p[index]
        pt[0] = pt[0].upper()

    def pointToRelative(self, index):
        pt = self.p[index]
        pt[0] = pt[0].upper()

    def getXPoint(self, index):
        pt = self.p[index]
        command = pt[0].upper()

        if self.pathdefs.has_key(command) is False:
            raise Exception, 'Invalid command'

        if command in ['M', 'L']:
            return pt[1][0]
        elif command == 'C':
            return pt[1][4]

