#!/usr/bin/env python
# -*- coding:utf-8 -*-
#login ssh interact
import pexpect
import termios
import datetime
import os
import sys
import time
import signal
import subprocess


def sigwinch_passthrough (sig, data):
    # Check for buggy platforms (see pexpect.setwinsize()).
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912 # assume
    s = struct.pack ("HHHH", 0, 0, 0, 0)
    a = struct.unpack ('HHHH', fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ , s))
    global global_pexpect_instance
    global_pexpect_instance.setwinsize(a[0],a[1])

def get_child_str(child):
    index=child.expect(['assword','group','account'])
    return index

def get_login_str(gstring,password):
    cmd='java -jar gauth.jar {0} {1}'.format(gstring,password)
    try:
        p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdoutput,erroutput) = p.communicate()
    except Exception as e:
        print e
    else:
        if stdoutput:
                return stdoutput
        if erroutput:
            print erroutput 
            exit(0)
def login_skip(user,host,password,dest_hostname):
    child=pexpect.spawn('ssh -A {0}@{1}'.format(user.strip(),host.strip()))
    index=child.expect('assword:')
    child.sendline(password)
    global global_pexpect_instance
    global_pexpect_instance = child
    if dest_hostname:
            index=child.expect('group:')
            child.sendline("/{0}".format(dest_hostname))
            index=child.expect('account:')
            child.sendline('2')
    child.interact()

        

if __name__=="__main__":
    args=sys.argv
    try:
        dest_hostname=args[1]
    except Exception as e:
        dest_hostname=''
    gstring=''
    password=''
    user='ertao.xu'
    host='192.168.21.250'
    password_login=get_login_str(gstring,password)
    login_skip(user,host,password_login,dest_hostname)
