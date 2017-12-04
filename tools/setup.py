#!/usr/bin/python3
import argparse
import configparser
import os,sys
import pprint

from os.path import realpath,join,dirname
sys.path.insert(0, join(dirname(realpath(__file__)), '../'))

from rta.provision import *

pp = pprint.PrettyPrinter(indent = 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='setup of Xiaogu RTA services',
        usage = '''
            set up influxdb: ./setup.py -c influxdb -d host -n orgName -p passwd -o 'db:db_name,key1=value,key2=value'
            set up grafana: ./setup.py -c grafana -d host:port -n orgName -p passwd
            set up kapacitor: ./setup.py -c kapacitor -d host:port -n orgName -p passwd
            set up rta-monitor: ./setup.py -c app -d host:port -n orgName -p passwd
            set up all: ./setup.py -c all -d host:port -n orgName -p passwd
        ''', formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-c', type = str, default='', help='provision component')
    parser.add_argument('-n', type = str, default='example', help='org name')
    parser.add_argument('-d', type = str, default='127.0.0.1:8086', help='destination host and port')
    parser.add_argument('-o', type = str, default ='', help='options for this operation')
    parser.add_argument('-db', type = str, default = '', help = 'influxdb database')

    args = parser.parse_args()
    component = args.c

    if component == "influxdb":
        create_influxdb_admin(args.n, args.p, args.d)
    else:
        sys.stderr.write('not recognized component, exit!\n')
        sys.exit(1)
