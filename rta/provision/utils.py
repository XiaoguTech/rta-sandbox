# -*- coding: utf-8 -*-
from random import choice
import string

def genPasswd(length=6, chars=string.ascii_lowercase + string.digits):
    return ''.join([choice(chars) for i in range(length)])
