from string import printable
from jft.pf import f as pf

# replace_unprintable
f = lambda ζ: ''.join([z if z in printable else '*' for z in ζ])
def t():
  x = [''.join([chr(x) for x in range(128)])][0]
  y = ''.join([
    '*********\t\n\x0b\x0c\r****************** !"#$%&\'()*+,-./0123456789:;',
    '<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~*'
  ])
  z = f(x)
  if y != z: return pf([
    'y != z',
    f'[y]: {[y]}',
    f'[z]: {[z]}'
  ])
  return y == z
