# -*- coding: utf-8 -*-
from rta.provision.utils import *
import sys,os
import requests
import time

def create_kapacitor(dest, options, conf_path):
    cp = "cp -r " + conf_path + "kapacitor /rta-conf/"
    docker = "docker run -d -p 9092:9092 -v /rta-data/kapacitor:/var/lib/kapacitor -v /rta-conf/kapacitor:/etc/kapacitor/ kapacitor"
    status = os.system(cp)
    if status != 0:
        err("E! error copy kapacitor config, exit")
        exit(1)
    
    cp = "cp -r %s../bin /rta-data/kapacitor" % conf_path
    status = os.system(cp)
    if status != 0:
        err("E! error copy kapacitor morgoth")
        exit(1)

    log('I! start deploying docker of kapacitor...')
    status = os.system(docker)
    if status != 0:
        err("E! error, exit")
        exit(1)
    log('I! finish deploying docker of kapacitor...')

