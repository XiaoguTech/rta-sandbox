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
            manage grafana: ./manage_grafana.py -d host:port -o create -t dashboard -n test_dash -username li3 -password 123q456w'
        ''', formatter_class = argparse.RawTextHelpFormatter)
    
    parser.add_argument('-o', type = str, default='create', help='operation, e.g. create/ delete')
    parser.add_argument('-t', type = str, default='dashboard', help='type, e.g. dashboard/ panel/ datasource')
    parser.add_argument('-d', type = str, default='127.0.0.1:3000', help='destination host and port')
    parser.add_argument('-n', type = str, help='type name')
    parser.add_argument('-username', type = str, default='li3', help='grafana username')
    parser.add_argument('-password', type = str, default ='123q456w', help='grafana password')
    
    args = parser.parse_args()
    
    manage_grafana(args.d, args.o, args.t, args.n, args.username, args.password)
