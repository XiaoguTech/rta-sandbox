# -*- coding: utf-8 -*-
from random import choice
import sys, os
import string

SUPERUSER   = 'XIAOGU'
SUPERPASSWD = 'XIAOGU'

log = sys.stdout.write
err = sys.stderr.write
def genPasswd(length=6, chars=string.ascii_lowercase + string.digits):
    return ''.join([choice(chars) for i in range(length)])
