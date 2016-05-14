#!/usr/bin/python

import unittest
from jenkinsports import commandArgs

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

if __name__ == '__main__':
    unittest.main()
