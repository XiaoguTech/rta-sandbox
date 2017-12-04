# -*- coding: utf-8 -*-
from rta.provision.utils import *
import sys,os

def create_passwd(orgName, options):
    passwd = genPasswd(6)
    if 'option' in options and options['option'] == 'samePasswd':
        passwd = orgName
    sys.stdout.write(passwd + '\n')
