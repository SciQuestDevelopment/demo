from scholarly import scholarly
search_query = scholarly.search_pubs("computer science")
list1 = []
for i in range(20):
    try:
        pub = next(search_query)
        list1.append(pub)
        print(pub)
    except:
        print("End of the iterator")
        break;
