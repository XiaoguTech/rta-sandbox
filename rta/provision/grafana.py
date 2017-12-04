from rta.provision.utils import *
import sys,os

def create_grafana(dest, options, conf_path):
    cp = "cp -r " + conf_path + "grafana /rta-conf/"
    docker = "docker run -d -p 3000:3000 -v /rta-data/grafana:/var/lib/grafana -v /rta-conf/grafana:/etc/grafana/ grafana/grafana"
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

    '''log('I! create superuser[xiaogu,xiaogu]')
    url = "http://%s:8086/query?q=create user %s with password '%s' with all privileges" % (dest, SUPERUSER, SUPERPASSWD)
    resp = requests.post(url)
    if resp.status_code != 200:
        err("E! Cannot create super-admin user! %s" % resp.text)
        exit(1)
    log('I! done for influxdb')'''
