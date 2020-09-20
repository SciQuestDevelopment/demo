import json

from scholarly import scholarly

query = scholarly.search_pubs("computer vision")
pub = next(query)

jsonStr = json.dumps(pub.bib)
print(jsonStr)
# print(type(pub.bibtex))
