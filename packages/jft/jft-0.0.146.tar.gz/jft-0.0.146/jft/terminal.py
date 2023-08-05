from jft.system.screen.clear import f as clear_screen
from jft.pf import f as pf

class Terminal:
  __init__ = lambda self, mode='run': self.reset(mode)

  def print(self, string:str='', end='\n'):
    if self.mode == 'test':
      self.output_stream_as_list.append(string+end)
    else:
      print(string, end=end)
    return string

  def input(self, string=''):
    if self.mode == 'test':
      return self.input_stream_as_list.pop()
    else:
      return input(string)

  def reset(self, mode='run'):
    self.reset_stream_lists()
    self.mode = mode

  def reset_stdo(self): self.output_stream_as_list = []
  def reset_stdi(self): self.input_stream_as_list = []

  def reset_stream_lists(self):
    self.reset_stdi()
    self.reset_stdo()
  
  def clear(self, cls=None):
    self.reset_stdo()
    return (clear_screen if self.mode == 'run' else lambda: True)()

f = lambda mode='run': Terminal(mode)

def test_clear():
  terminal = f('test')
  terminal.print('abc')
  result = terminal.clear()
  return all([terminal.output_stream_as_list == [], result])

def test_terminal_print():
  terminal = f('test')
  data = 'abc'
  result = terminal.print(data)

  if terminal.output_stream_as_list != [data+'\n']: return pf([
    'terminal.output_stream_as_list != [data+"\n"]',
    f'terminal.output_stream_as_list: {terminal.output_stream_as_list}',
    f'[data]:                         {[data]}'
  ])

  if result != data: return pf([
    'result != data',
    f'[result]: {[result]}',
    f'[data]:   {[data]}'
  ])
  
  return True

def test_terminal_input():
  terminal = f('test')
  terminal.input_stream_as_list.append('response text')
  returned_value = terminal.input('prompt text')
  return returned_value == 'response text'

def test_terminal_reset():
  terminal = f('test')

  terminal.mode = 'xyz'
  terminal.input_stream_as_list.append('abc')
  terminal.output_stream_as_list.append('ghi')
  terminal.reset()
      
  return all([
    terminal.mode == 'run',
    terminal.input_stream_as_list == [],
    terminal.output_stream_as_list == []
  ])

def test_terminal_reset_stdo():
  terminal = f('test')
  terminal.output_stream_as_list.append('ghi')
  terminal.reset_stdo()
  return terminal.output_stream_as_list == []

def test_terminal_reset_stdi():
  terminal = f('test')
  terminal.input_stream_as_list.append('ghi')
  terminal.reset_stdi()
  return terminal.input_stream_as_list == []

def test_terminal_reset_stream_lists():
  terminal = f('test')
  terminal.output_stream_as_list.append('abc')
  terminal.input_stream_as_list.append('ghi')
  terminal.reset_stream_lists()
  return all([
    terminal.output_stream_as_list == [],
    terminal.input_stream_as_list == []
  ])

def t():
  if not test_terminal_print(): return pf(['not test_terminal_print()'])
  if not test_terminal_input(): return pf(['not test_terminal_input()'])
  if not test_terminal_reset(): return pf(['not test_terminal_reset()'])
  if not test_terminal_reset_stdo(): return pf(['!test_terminal_reset_stdo()'])
  if not test_terminal_reset_stdi(): return pf(['!test_terminal_reset_stdi()'])

  if not test_terminal_reset_stream_lists(): return pf([
    'not test_terminal_reset_stream_lists()'
  ])

  if not test_clear(): return pf(['not test_clear()'])
  return True
