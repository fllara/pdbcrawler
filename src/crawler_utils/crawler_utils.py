class crawler_utils(object):
  '''
  Placeholder for useful methods and constants.
  '''
  @staticmethod
  def chunkenize_1D(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
      yield lst[i:i + n]
  
  @staticmethod
  def is_notebook() -> bool:
    try:
      shell = get_ipython().__class__.__name__
      if shell == 'ZMQInteractiveShell' or 'google.colab' in get_ipython().__module__:
          return True   # Jupyter notebook or qtconsole
      elif shell == 'TerminalInteractiveShell':
          return False  # Terminal running IPython
      else:
          return False  # Other type (?)
    except NameError:
      return False