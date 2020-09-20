from json import JSONEncoder

from scholarly import scholarly
import json

search_query = scholarly.search_author('Marty Banks')
author = next(search_query)

author.fill(sections=['publications'])
lens = len(author.publications)
pub = author.publications[0:50]
print(pub)
pub = str(pub).replace('\n','')
pub = ' '.join(pub.split())
data = {'name': author.name, 'affilication': author.affiliation, 'email': author.email, 'picture':author.url_picture ,'publications': pub }
jsonStr = json.dumps(data)
print(jsonStr)

