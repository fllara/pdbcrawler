from crawler_utils.query import Query
from crawler_utils.crawler_utils import *

import pandas as pd
import urllib, re
import aiohttp
import asyncio
from copy import deepcopy
import typing as tp
class PDBCrawler(object):
  def __init__(self, 
               query: Query,
               **kwargs
               ) -> None:
    
    self.is_notebook = crawler_utils.is_notebook()
    # change this urgent! dangerous behavior
    if self.is_notebook:
      # URGENT!! Change this!!
      try:
        import nest_asyncio
        nest_asyncio.apply()
      except ImportError as e:
        print("## Could not import and set nest_asyncio. Check package installation.")
        raise e
    self.loop = asyncio.get_event_loop()
    self.set_base_query(query)
    self.query_generator = None 

  async def get_rcsb_query(self, session, query):
    async with session.get(query) as resp:
        if resp.status == 200:
          response = await resp.json()
        else: 
          body = await resp.read()
          response = f'Error, status: {resp.status} | msg: {body.decode()}'    
          
        return response

  def set_base_query(self, base_query: tp.Union[str, Query]) -> None:
    # this method is at stand by right now.
    if isinstance(base_query, Query):
      self.query = base_query
    else:
      try:
        self.query = Query(base_query=base_query)
      except Exception as e:
        print('!! Error creatinng Query Object !!')
        raise e
    return
    
  def _get_query_generator(self, 
                          ids_list: list=None, 
                          chunksize: int=1000):
    # this method is ugly now
    # it will become a static method 
    #if not query_obj:
    assert self.query, "# self.query not set (None)."
    query_obj = deepcopy(self.query)
    # if not ids_list:
    #   assert self.ids_list, "# Both ids_list and self.ids_list are None. Cannot run without a ids."
    #   ids_list = self.ids_list # no deepcopy needed here.

    iterator = crawler_utils.chunkenize_1D(ids_list, chunksize)
    preproc = lambda l: ','.join([f'''"{p}"''' for p in l])
    for chunk in iterator:
      qparms = {'@IDS': chunk}
      qparms['@IDS'] = preproc(qparms['@IDS'])
      query_obj.setup_query(qparms=qparms, inplace=True)
      query_obj.encode_query(inplace=True)
      yield query_obj.query 

  
  async def _get_query_data(self, prep_methods: list=None, **generator_kwargs) -> None:
    '''
    Work out this method to accept qparms instead, and generate the
    query with these qparms.
    Generator kwargs --> perigoso...
    '''
  
    self.query_generator = self._get_query_generator(**generator_kwargs)
    self.session = aiohttp.ClientSession()
    tasks = []
    for chunk in self.query_generator:
      url = f'https://data.rcsb.org/graphql?query={chunk}'
      task = self.get_rcsb_query(self.session, url)
      #if prep_methods:
      task = asyncio.ensure_future(self.response_prep(task, [lambda x: x]))
      tasks.append(task)
      #tasks.append(self.get_rcsb_query(self.session, url))
    
    #result = await asyncio.gather(*tasks)
    result = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
    self.query_generator = None # restarts self.query_generator to initial state
    return result

  async def response_prep(self,
                          response: str,
                          prep_methods: tp.Union[list,tp.Callable]
                           ) -> list:
    for prep in prep_methods:
      response = await prep(response)
    return response

  def get_data(self,
               ids_list: list,
               chunksize: int=1000,
               parse_response: bool=True) -> list:    
    response = self._get_query_data(ids_list=ids_list, chunksize=chunksize)
    response = self.loop.run_until_complete(response)
    asyncio.run(self.session.close())
    if parse_response:
      print(f'Parsing {len(response)} responses.')
      response, errors = crawler_utils.parsePDBResponse(response)
      if errors: print(f'{len(errors)} Error(s) was/were found!')
    return response
    
      

    