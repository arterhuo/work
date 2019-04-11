#!/usr/bin/env python
# -*- coding:utf-8 -*-
#login ssh interact
from optparse import OptionParser
import re
import pexpect
import termios
import datetime
import os
import sys
import time
import signal
import subprocess
import struct
import fcntl
global child

def sigwinch_passthrough (sig, data):

    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    winsize = struct.unpack('HHHH', x)[0:2]

    global child
    child.setwinsize(winsize[0],winsize[1])

def login_skip(host,dest_hostname):
    global child
    child=pexpect.spawn('ssh {0}'.format(host.strip()))
    child.setecho(False) #dublicates spawn call (trying to force)
    index=child.expect('Opt>')
    child.sendline("/{0}".format(dest_hostname))
    index=child.expect('Opt>')
    output=child.before
    match=re.search(r'总共: \d+ 匹配: (\d+)',output)
    if match and int(match.group(1)) == 1:
        sendline = '1'
    else:
        sendline = "/{0}".format(dest_hostname)
    child.sendline(sendline)
    child.before.strip(sendline)
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    child.interact()

if __name__=="__main__":
    usage = "usage: %prog dest_hostname"
    parser = OptionParser(usage=usage)
    (options, args) = parser.parse_args()
    try:
        dest_hostname = args[0]
    except Exception as e:
        parser.print_help()
        exit(-1)
    host='jump'
    if dest_hostname:
        login_skip(host,dest_hostname)
    else:
        parser.print_help()
