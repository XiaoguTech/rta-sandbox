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
    def post(url):
        res = requests.post(url)
        if res.status_code != 200:
            log(res.text)
    # create database
    super_url = "http://%s/query?u=%s&p=%s&q=" % (dest, SUPERUSER, SUPERPASSWD)
    url = super_url + 'create database ' + database
    post(url)

    # create a normal user
    url = super_url + 'create user %s with password \'%s\'' % (username, password)
    post(url)

    # grant privileges to the normal user
    url = super_url + 'grant ALL on %s to %s' % (database, username)
    post(url) 


def manage_influxdb(dest, username, password, database, measurement, option, rps=[], rp_names=[], cqs=[], cq_names=[]):
    def post(query_clause):
        url = "http://%s/query?u=%s&p=%s&db=%s&q=%s" % (dest, username, password, database, query_clause)
        res = requests.post(url)
        if res.status_code == 200:
            err(res.text)
            sys.exit(1)

    # delete a measurement and return
    if option == 'delete':
        post('drop measurement ' + measurement)
    elif option == 'add':
        if len(rps) != len(cqs) + 1:
            err('E! Retention policy count error!')
            sys.exit(1)
        for index, rp in enumerate( list(zip(rp_names, rps)) ):
            post('create retention policy %s on %s duration %s replication' % (rp[0], database, rp[1]) )

        continuous_create_format = 'create continuous query {cq_name} on %s begin select mean(*) into {retention}.%s from {last_retention}.%s group by time({cq_time}), * end' % (database, measurement, measurement)
        for i in range(len(cqs)):
            cq = continuous_create_format.format(cq_name=cq_names[i], retention=rp_names[i+1], last_retention=rp_names[i], cq_time=cqs[i])
            post(cq)
        
