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
            manage influxdb: ./manage_influxdb.py -db lee -m test -rp 1d,1w,8w -rpn rp_1d,rp_1w,rp_8w -cq 5m,1h -cqn cq_5m,cq_1h -o add/delete -username lee -password 123 -d host:port'
        ''', formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-o', type = str, default='example', help='option name')

    parser.add_argument('-d', type = str, default='127.0.0.1:8086', help='destination host and port')
    parser.add_argument('-db', type = str, default='lee', help='manipulated database')
    parser.add_argument('-m', type = str, default='127.0.0.1:8086', help='manipulated measurement')
    parser.add_argument('-username', type = str, default='127.0.0.1:8086', help='database admin username')
    parser.add_argument('-password', type = str, default ='', help='database admin password')
    
    parser.add_argument('-rp', type = str, default='1d,1w,8w', help='retention policy, split with ,')
    parser.add_argument('-rpn', type = str, default='rp_1d,rp_1w,rp_8w', help='retention policy names, split with ,')
    parser.add_argument('-cq', type = str, default='5m,5h', help='continuous query, split with ,')
    parser.add_argument('-cqn', type = str, default='cq_5m,cq_5h', help='continuous query names, split with ,')
    args = parser.parse_args()
    
    manage_influxdb(args.d, args.username, args.password, args.db, args.m, args.o, args.rp.split(','), args.rpn.split(','), args.cq.split(','), args.cqn.split(','))

