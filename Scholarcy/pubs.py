from scholarly import scholarly
search_query = scholarly.search_pubs(year_low=2018, query="computer science",)
list1 = []
for i in range(20):
    try:
        pub = next(search_query)
        list1.append(pub)
        print(pub)
    except:
        print("End of the iterator")
        break;
# import html
# s = "graphene &quot;advanced science&quot; source:advanced source:science"
# temp = html.unescape(s)
# print(temp)