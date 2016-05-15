#!/usr/bin/python

import yaml
import sys
import argparse

ERR_OPENING_CONF   = 1
ERR_UNKNOWN_JOB    = 2
ERR_DUPLICATE_PORT = 3

def isIterable(varToCheck):
  retValue=True
  try:
    _ = (e for e in varToCheck)
  except:
    retValue=False
  return retValue

def commandArgs(cmdLine):
  parser = argparse.ArgumentParser(description='Jenkins Port Register')
  parser.add_argument('-f','--file',help='Register file')
  parser.add_argument('job name',nargs=1,help='Jenkins Job Name')
  args = parser.parse_args(cmdLine)
  return args

def validateConf(conf):
  portList=[]
  if isIterable(conf) > 0:
    for job in conf:
      for port_no in conf[job]:
        if conf[job][port_no] in portList:
          print "Duplicate port %s in conf" % (str(conf[job][port_no]))
          return(ERR_DUPLICATE_PORT)
        else:
          portList.append(conf[job][port_no])
  return 0

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
    return(ERR_OPENING_CONF)

  valid=validateConf(conf)
  if valid != 0:
    return valid
 
  job_found=False
 
  if isIterable(conf):
    for job in conf:
      if str(job) == str(vars(args)['job name'][0]):
        job_found=True
        for port_no in conf[job]:
          print "export " + str(port_no) + "=" + str(conf[job][port_no])
        return(0)
  
  if job_found==False:
    print "Job not in config file"
    return(ERR_UNKNOWN_JOB)

if __name__ == '__main__':
  args=commandArgs(sys.argv[1:])
  sys.exit(jenkinsPorts(args))
