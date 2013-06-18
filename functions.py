#!/usr/bin/env python

import os
import sys
import subprocess
import tempfile
import re

def run(command):
        tmpfile = tempfile.mktemp()
        command = command + ' > ' + tmpfile
        msg = None
        data = None

        try:
                from subprocess import Popen, PIPE
                p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
                rc = p.wait()
                out = p.stdout.read()
                err = p.stderr.read()
        except ImportError:
                try:
                        from popen2 import Popen3
                        p = Popen3(command, True)
                        p.wait()
                        rc = p.poll()
                        out = p.fromchild.read()
                        err = p.childerr.read()
                except ImportError:
                        msg = "Neither subprocess.Popen nor popen2.Popen3 is available"

        if msg is None:
                try:
                        f = open(tmpfile, "rb")
                        data = f.read()
                        f.close()
                except IOError, inst:
                        msg = "Error reading temporary file: %s" % str(inst)

        if msg is not None:
                sys.stdout.write(msg)

        if data is not None:
                return data

        return None

def getDimensions(inputfile, id):
        command = 'inkscape --query-all %s'
        data = run(command % inputfile)
        regex = re.compile('%s.*' % id, re.MULTILINE)
        m = regex.search(data)
        if m is not None:
                return re.split(',', m.group())
        else:
                return ['', 0, 0, 0, 0]

