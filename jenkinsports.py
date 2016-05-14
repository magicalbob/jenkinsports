#!/usr/bin/python

import yaml
import sys
import argparse

def commandArgs(cmdLine):
  parser = argparse.ArgumentParser(description='Jenkins Port Register')
  parser.add_argument('-f','--file',help='Register file')
  parser.add_argument('job name',nargs=1,help='Jenkins Job Name')
  args = parser.parse_args(cmdLine)
  return args

def jenkinsPorts(args):
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
 
  job_found=False
 
  try:
    for job in conf:
      if str(job) == str(vars(args)['job name'][0]):
        job_found=True
        for port_no in conf[job]:
          print "export " + str(port_no) + "=" + str(conf[job][port_no])
        sys.exit(0)
  except:
    # print "Unexpected error:", sys.exc_info()[0]
    pass
  
  if job_found==False:
    print "Job not in config file"
    sys.exit(2)

if __name__ == '__main__':
  args=commandArgs(sys.argv[1:])
  jenkinsPorts(args)
