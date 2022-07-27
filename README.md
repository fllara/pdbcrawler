# pdbcrawler
A simple interface to crawl RCSB PDB database painlessly.
This crawler is part of my master's work and was born out of the need to download information about proteins fast and easy. For now it consists of basically 2 classes that take care of the query parsing, parameterizing and RCSB API requests (crawl). Take a look at the `Future` section to see the next improvements. And feel free to make pull requests for functionalities. <br>
<br>
### What it does? How it works?
RCSB provides a public access API to their GraphQL (a graph oriented database). The problem is that building queries is not that intuitive and most Biologists, BIophysicists, Bioinformaticians are not used to construct queries. By creating a `Query` object we can easily standarize query building and accelerate information retrieval. No need to spend time developing queries here and there. Just input what kind of information you want, the proteins and that's it. <br>
**Current State**: for now we only fetch Molecular Weight data about proteins, but we'll add other info. (Check **Future** to have a glimpse of what is comming)

# Requirements:
- Python 3 (tested and developed in 3.8)
- aiohttp
- pandas 

# How to use?
Just import the 3 classes (`Query`, `PDBCrawler` and `crawler_utils`), setup a `Query` object with a parameterized query (more on this later), feed this `Query` while creating a `PDBCrawler` and run `PDBCrawler.get_data` and **voi lá**! <br>

# Code example
```python
import Query, PDBCrawler, crawler_utils

with open('queryfile', 'r') as qfile:
  query = Query(base_query = f.read())

# you can generate this list with whatever methods you'd like.
list_of_prots = ['protA', 'protB', ..., 'protZ'] # list of 10k proteins

crawler = PDBCrawler(base_query)

data = crawler.get_data(ids_list=list_of_prots, chunksize=100) # get chunks of 100 responses at a time async
```
# Future
0. Adopt `GitFlow` versioning;
1. Create standard `Crawler` class, from which every api querying system will inherit
2. Add `QueryResponse` class, to standarize query responses from `Crawler.get_data()`
3. Add `qparms` (dictionary of query parameters) support to `Crawler.get_data` and `Crawler.
4. Add `qproc` (a processing module to apply to each responde) support to `Crawler`
5. Create `UNIPROTCrawler` class;
6. Create `IDMapper` class, to map from `rcsb_id` to `uniprot_kb`.
7. Create `Serializer` class, to orchestrate data serialization.

