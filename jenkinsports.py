#!/usr/bin/python

import yaml
import sys
import argparse

parser = argparse.ArgumentParser(description='Jenkins Port Register')
parser.add_argument('-f','--file',help='Register file')
parser.add_argument('job name',nargs=1,help='Jenkins Job Name')
args = parser.parse_args()

if vars(args)['file'] == None:
  conf_file='jenkinsports.yml'
else:
  conf_file=vars(args)['file']

try:
  with open(conf_file,'r') as confile:
    conf = yaml.load(confile)
except:
  print "Error: opening config file " + conf_file
  sys.exit(1)

for job in conf:
  if str(job) == str(vars(args)['job name'][0]):
    for port_no in conf[job]:
      print "export " + port_no + "=" + conf[job][port_no]
    sys.exit(0)

sys.exit(2)
