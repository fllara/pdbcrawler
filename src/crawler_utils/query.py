import urllib, re
from copy import deepcopy
import typing as tp

class Query(object):
  def __init__(self, base_query, **kwargs):
    self.set_base_query(base_query)
    self.query_params = kwargs.pop('query_params', None)
    self.query_preproc_methods = kwargs.pop('query_preproc_methods', None)
    if not self.query_params:
      print(f'!! WARNING !! No query parameters dict were supplied.')
    self.query = None # the latest state of query object
    # provisório
    self.nodes = None # nodes são nós no gráfico: rcsb_entry_info, poly
    

  def encode_query(self, inplace=False):
    if not self.query:
      raise AttributeError('self.query Not set. You must run setup_query first!')
    self.query = urllib.parse.quote(self.query)
    return deepcopy(self) if not inplace else None
  
  def set_base_query(self, base_query):
    if '@' not in base_query:
      raise TypeError(f'# Base query does not contains parameter identifier (@)')
    self.base_query = base_query

  def __set_query(self, query, inplace=False):
    self.query = query
    return deepcopy(self) if not inplace else None

  def setup_query(self, 
                qparms: dict=None,
                url_quote: bool=False,
                inplace=False) -> str:
    '''
    Setup a string query and maps {qparms} to whatever parameter identifier(`@parm`) inside.
    Args:
      query: (str) the graphQL query to pdb
      qparms: (dict) a dictionary containing Parameter Information (value) by (key)
      qpreproc: (dict) if None, assumes the qparms are already preproc'd, else
      tries to preproc the parms. In case something goes wrong, returns empty
      string, as this is an error.
      url_quote: (bool) wether or not to URL-encode query (RFC 3986 compliant)
    '''
    if not qparms:
      qparms = self.query_params
    query = re.sub("\s+", '', self.base_query)
    try:
      # tries to sub every parameter from qparms into query
      query = re.sub("@\w+", lambda m: qparms.get(m.group(), m.group()), query)
    except KeyError as e:
      print(f'!! Query assembly error. Parameter issues. (returning '') | Type: {repr(e)}')
      query = ''
    except Exception as e:
      print(f"!! Generic error (returning '') | Type: {repr(e)}")
      query = ''
    
    if inplace:
      self.__set_query(query)
      return None
    return deepcopy(self).__set_query(query)
  