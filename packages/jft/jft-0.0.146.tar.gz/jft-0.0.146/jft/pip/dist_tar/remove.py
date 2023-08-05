from os.path import exists
from jft.directory.remove import f as rmdirie
from jft.directories.make import f as mkdirsine

temp_root = './_dist_tars_remove'
target = f'{temp_root}/dist'

def setup(): mkdirsine([temp_root, target])

def tear_down(): rmdirie(temp_root)

def t():
  setup()
  f(temp_root)
  result = all([not exists(target), exists(temp_root)])
  tear_down()
  return result

def f(x='.'): rmdirie(f'{x}/dist')
