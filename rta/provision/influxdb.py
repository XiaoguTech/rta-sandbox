# -*- coding: utf-8 -*-
from rta.provision.utils import *
import sys,os
import requests


def create_influxdb(dest, options, conf_path):
    cp = "cp -r " + conf_path + "influxdb /rta-conf/"
    docker = "docker run -d -p 8086:8086 -v /rta-data/influxdb:/var/lib/influxdb -v /rta-conf/influxdb:/etc/influxdb influxdb"
    log(cp)
    log(docker)
    os.system(cp)
    os.system(docker)
    
    url = "http://%s:8086?q=create user %s with password '%s' with all privileges" % (dest, SUPERUSER, SUPERPASSWD)
    resp = requests.post(url)
    if resp.status_code != 200:
        err("E! Cannot create super-admin user!")
