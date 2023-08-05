from importlib import import_module
from jft.directory.make import f as mkdirine
from jft.directory.remove import f as rmdirie
from jft.file.save import f as save

_dir = './_pi_test_failed'
_expected_pass_pi_path = f'{_dir}/_expected_pass.py'
_expected_fail_pi_path = f'{_dir}/_expected_fail.py'

def setup():
  mkdirine(_dir)
  save(_expected_pass_pi_path, 'f = lambda: None\nt = lambda: True')
  save(_expected_fail_pi_path, 'f = lambda: None\nt = lambda: False')

def tear_down(): rmdirie(_dir)

f = lambda x: not import_module(x.replace('/','.').replace('..','')[:-3]).t()

def t():
  setup()
  result = all([not f(_expected_pass_pi_path), f(_expected_fail_pi_path)])
  tear_down()
  return result
