from rta.provision.utils import *
import sys,os
import requests, json

def create_grafana(dest, options, conf_path):
    cp = "cp -r " + conf_path + "grafana /rta-conf/"
    docker = "docker run -d -p 3000:3000 -v /rta-data/grafana:/var/lib/grafana -v /rta-conf/grafana:/etc/grafana/ grafana/grafana"
    status = os.system(cp)
    if status != 0:
        err("E! error, exit")
        exit(1)
    
    log('I! start deploying docker of grafana...')
    status = os.system(docker)
    if status != 0:
        err("E! error, exit")
        exit(1)
    log('I! finish deploying docker of grafana...')

def create_grafana_admin(dest, username, password, org):
    def check(res):
        log(res.text)
        if res.status_code != 200:
            sys.exit(1)

    base_url = "http://%s:%s@%s/" % (SUPERUSER, SUPERPASSWD, dest)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    # First, create a normal user.
    url = base_url + 'api/admin/users'
    data = {
        "name": username,
        "login": username,
        "password": password
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    check(res)
    
    # Create an organisation for the user
    url = base_url + 'api/orgs'
    data = {
        "name": org
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    check(res)
    orgId = res.json()["orgId"]
    log('\norgId' + str(orgId) + '\n')

    # Switch current org
    url = base_url + 'api/user/using/' + str(orgId)
    res = requests.post(url, headers=headers)
    check(res)

    # Add current user to the org with admin privileges
    url = base_url + 'api/org/invites'
    data = {
        "name": "", "email": "", 
        "role": "Admin",
        "loginOrEmail": username,
        "skipEmails": True
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Switch current user org
    url = "http://%s:%s@%s/api/user/using/" % (username, password, dest)+ str(orgId)
    res = requests.post(url, headers=headers)
    check(res)


def manage_grafana(dest, option, tp, title, username, password, clone=None):
    base_url = "http://{user}:{password}@{host}/".format(user=username, password=password, host=dest)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    def create_dashboard():
        template = {
            "dashboard": {
                "id": None,
                "title": title,
                "tags": [ "templated" ],
                "timezone": "browser",
                "rows": [
                    {
                    }
                ],
                "schemaVersion": 6,
                "version": 0
            },
            "overwrite": False
        }
        url = base_url + 'api/dashboards/db'
        res = requests.post(url, headers=headers, data=json.dumps(template))
        if res.status_code == '412':
            err('E! Dashboard has existed!')
        else:
            check(res)

    def delete_dashboard():
        pass

    # Reflection, for multi manipulate
    func = "{option}_{tp}()".format(option=option, tp=tp)
    eval(func)
