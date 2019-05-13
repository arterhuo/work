#!/usr/bin/env python
# -*- coding:utf-8 -*-
#login ssh interact
#author by ertao.xu
from optparse import OptionParser
import getpass
import sys
import re
import pexpect
import termios
import signal
import struct
import fcntl
import commands
import time

def sigwinch_passthrough (sig, data):
    win = winsize()
    global global_pexpect
    global_pexpect.setwinsize(win[0],win[1])

def winsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

def GetMFA():
    PassMFA = commands.getoutput("cd ~/git/work && java -jar ~/git/work/gauth.jar")
    return PassMFA.split()

def while_expect(child):
    passwd,mfa = GetMFA()
    index=child.expect(['Opt>','password:','\[MFA auth\]:']) 
    if index == 0:
        print child.before+'Opt>',
        return child
    elif index == 1:
        #child.sendline(getpass.getpass(prompt=child.before+"password:"))
        child.sendline(passwd)
        while_expect(child)
    elif index == 2:
        child.sendline(mfa.strip())      
        #child.sendline(raw_input(child.before+"[MFA auth]:"))
        while_expect(child)

def login_skip(host,dest_hostname):
    child=pexpect.spawn('ssh {0}'.format(host.strip()))
    child.setecho(False)
    while_expect(child)
    child.sendline("{0}".format(dest_hostname))
    global global_pexpect
    global_pexpect = child
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    win = winsize()
    global_pexpect.setwinsize(win[0],win[1])
    global_pexpect.interact()

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
