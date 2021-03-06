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
        description='provision of Xiaogu RTA services',
        usage = '''
            genPasswd: ./provision.py -c passwd -n orgName -o 'option:samePasswd'
            set up influxdb: ./provision.py -c influxdb -d host -n orgName -p passwd -o 'db:db_name,key1=value,key2=value'
            set up grafana: ./provision.py -c grafana -d host:port -n orgName -p passwd
            set up kapacitor: ./provision.py -c kapacitor -d host:port -n orgName -p passwd
            set up rta-monitor: ./provision.py -c app -d host:port -n orgName -p passwd
            set up all: ./provision.py -c all -d host:port -n orgName -p passwd
        ''', formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-c', type = str, default='', help='provision component')
    parser.add_argument('-n', type = str, default='example', help='org name')
    parser.add_argument('-d', type = str, default='127.0.0.1', help='destination host and port')
    parser.add_argument('-o', type = str, default ='', help='options for this operation')

    args = parser.parse_args()
    component = args.c

    if args.n == '':
        sys.stderr.write('please specify orgName with -n option\n')
        sys.exit(1)

    orgName = args.n

    options = {}
    if args.o != '':
        for option in args.o.split(','):
            (k,v) = option.split(':')
            options[k] = v
    working_path = join(dirname(realpath(__file__)), '../')
    print(working_path)
    conf_path = working_path + 'conf/'
    if component == 'passwd':
        create_passwd(orgName, options)
    elif component == 'influxdb':
        create_influxdb(args.d, options, conf_path)
    elif component == 'grafana':
        create_grafana(args.d, options, conf_path)
    elif component == 'kapacitor':
        create_kapacitor(args.d, options, conf_path)
    elif component == 'app':
        pass
    elif component == 'all':
        pass
    else:
        sys.stderr.write('not recognized component, exit!\n')
        sys.exit(1)

