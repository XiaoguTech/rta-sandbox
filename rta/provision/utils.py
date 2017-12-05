# -*- coding: utf-8 -*-
from random import choice
import sys, os
import string

SUPERUSER   = 'xiaogu'
SUPERPASSWD = 'xiaogu'

log = sys.stderr.write
err = sys.stderr.write
def genPasswd(length=6, chars=string.ascii_lowercase + string.digits):
    return ''.join([choice(chars) for i in range(length)])

def check(response):
    if response.status_code != 200:
        err('E!' + response.text)
        sys.exit(1)
