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
            set up influxdb: ./setup.py -retention_policy 1d,1w,4w -down_sampling 5m,1h -o add/delete -username lee -password 123 -d host:port -db lee -m measurement'
        ''', formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-c', type = str, default='', help='config dict')
    parser.add_argument('-o', type = str, default='example', help='option name')
    parser.add_argument('-username', type = str, default='127.0.0.1:8086', help='destination host and port')
    parser.add_argument('-password', type = str, default ='', help='options for this operation')
    
    args = parser.parse_args()
    component = args.c
    
    influx()

