# -*- coding: utf-8 -*-
from rta.provision.utils import *
import sys,os
import requests
import time

def create_influxdb(dest, options, conf_path):
    cp = "cp -r " + conf_path + "influxdb /rta-conf/"
    docker = "docker run -d -p 8086:8086 -v /rta-data/influxdb:/var/lib/influxdb -v /rta-conf/influxdb:/etc/influxdb influxdb"
    status = os.system(cp)
    if status != 0:
        err("E! error, exit")
        exit(1)
    
    log('I! start deploying docker of influxdb...')
    status = os.system(docker)
    if status != 0:
        err("E! error, exit")
        exit(1)
    time.sleep(5)
    log('I! finish deploying docker of influxdb...')

    log('I! create superuser[xiaogu,xiaogu]')
    url = "http://%s:8086/query?q=create user %s with password '%s' with all privileges" % (dest, SUPERUSER, SUPERPASSWD)
    resp = requests.post(url)
    if resp.status_code != 200:
        err("E! Cannot create super-admin user! %s" % resp.text)
        exit(1)
    log('I! done for influxdb')


def create_influxdb_admin(dest, username, password, database):
    url = "http://%s/query?u=%s&p=%s&q=create database %s" % (dest, username, password, database)
    res = requests.get(url)
    if res.status_code != 200:
        log(res.text)
