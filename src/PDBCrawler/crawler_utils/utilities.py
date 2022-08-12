import typing as tp
import pandas as pd
import tqdm

class CrawlerUtils(object):
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

  @staticmethod
  def getFieldNodes(nodes: dict, query: set) -> list:
    # gets the first value of matching key (is query in key)
    try:
      return next(node for fields, node in a.items() if query.issubset(fields))
    except StopIteration:
      return []
    except Exception as e:
      raise e

  @staticmethod
  def parsePDBResponse(responses: list, return_errors: bool=True) -> tp.Union[pd.DataFrame, list]:
    def RecordParser(response: dict) -> pd.DataFrame:
      return pd.json_normalize(response, 
                        record_path = ['data','entries', 'polymer_entities'], 
                        meta=[['data','entries','rcsb_id'], 
                              ['data','entries', 'pdbx_vrpt_summary', 'PDB_resolution'],
                              ['data','entries', 'rcsb_entry_info', 'molecular_weight']
                              ]
                        )

    parsed_response = pd.DataFrame()
    error_responses = list() if return_errors else None
    for record in tqdm.tqdm(responses):
      try:
        response = RecordParser(record)
      except Exception as e:
        if return_errors:
          error_responses.append(record)
      else:
        parsed_response = parsed_response.append(response)
    return parsed_response, error_responses