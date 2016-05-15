#!/usr/bin/python

import unittest
from jenkinsports import commandArgs
from jenkinsports import jenkinsPorts
import sys
from StringIO import StringIO
import tempfile

class JenkinsPortsTestCase(unittest.TestCase):
  def setUp(self):
    """setup ready for tests"""

  def tearDown(self):
    """Tidy up after tests"""

  def test_no_arguments(self):
    """No arguments"""
    try:
      args=commandArgs('')
    except:
      pass

    if 'args' in vars():
      self.fail()
    else:
      pass

  def test_one_job_argument(self):
    """One job name"""
    jname='a job'
    try:
      args=commandArgs([jname])
    except:
      pass

    if 'args' in vars():
      assert(vars(args)['job name'][0]==jname)
    else:
      self.fail()

  def test_just_file_argument(self):
    """Just file argument"""
    try:
      args=commandArgs(['-f','my.conf'])
    except:
      pass

    if 'args' in vars():
      self.fail()
    else:
      pass

  def test_all_arguments(self):
    """All arguments"""
    try:
      args=commandArgs(['-f','my.conf','my.job'])
    except:
      pass

    if 'args' in vars():
      assert(vars(args)['job name'][0]=='my.job')
      assert(vars(args)['file']=='my.conf')
    else:
      self.fail()

  def test_no_config(self):
    """Config file doesn't exist"""
    args=commandArgs(['-f','my.conf','my.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    assert output == 'Error: opening config file my.conf'
    sys.stdout = saved_stdout

  def test_unknown_job(self):
    """Job not in config file"""
    myconfig=tempfile.mkstemp()

    args=commandArgs(['-f',myconfig[1],'my.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    retCode=jenkinsPorts(args) 

    output = out.getvalue().strip()
    assert output == 'Job not in config file'
    sys.stdout = saved_stdout

  def test_job_one_port(self):
    """Job in config file with one port set"""
    myconfig=tempfile.mkstemp()
    with open(myconfig[1],"w") as config_file:
      config_file.write('my.job:\n  port1: 12345\n')

    args=commandArgs(['-f',myconfig[1],'my.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    sys.stdout = saved_stdout
    assert output == 'export port1=12345'

  def test_job_two_port(self):
    """Job in config file with two ports set"""
    myconfig=tempfile.mkstemp()
    with open(myconfig[1],"w") as config_file:
      config_file.write('my.job:\n  port1: 12345\n  port2: 23456\n')

    args=commandArgs(['-f',myconfig[1],'my.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    sys.stdout = saved_stdout
    assert output == 'export port2=23456\nexport port1=12345'

  def test_two_jobs_first(self):
    """Job in config file, first of 2 jobs"""
    myconfig=tempfile.mkstemp()
    with open(myconfig[1],"w") as config_file:
      config_file.write('right.job:\n  port1: 12345\n  port2: 23456\n')
      config_file.write('wrong.job:\n  port1: 34567\n  port2: 45678\n')

    args=commandArgs(['-f',myconfig[1],'right.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    sys.stdout = saved_stdout
    assert output == 'export port2=23456\nexport port1=12345'

  def test_two_jobs_last(self):
    """Job in config file, first of 2 jobs"""
    myconfig=tempfile.mkstemp()
    with open(myconfig[1],"w") as config_file:
      config_file.write('wrong.job:\n  port1: 12345\n  port2: 23456\n')
      config_file.write('right.job:\n  port1: 34567\n  port2: 45678\n')

    args=commandArgs(['-f',myconfig[1],'right.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    sys.stdout = saved_stdout
    assert output == 'export port2=45678\nexport port1=34567'

  def test_duplicate_port(self):
    """Job in config file, first of 2 jobs"""
    myconfig=tempfile.mkstemp()
    with open(myconfig[1],"w") as config_file:
      config_file.write('wrong.job:\n  port1: 12345\n  port2: 23456\n')
      config_file.write('right.job:\n  port1: 23456\n  port2: 45678\n')

    args=commandArgs(['-f',myconfig[1],'right.job'])

    saved_stdout = sys.stdout
    out = StringIO()
    sys.stdout = out

    try:
      jenkinsPorts(args) 
    except:
      pass

    output = out.getvalue().strip()
    sys.stdout = saved_stdout
    assert output == 'Duplicate port 23456 in conf'

if __name__ == '__main__':
    unittest.main()
