from scholarly import scholarly

# Retrieve the author's data, fill-in, and print
search_query = scholarly.search_author('Steven')
list1 = []
for i in range(20):
    try:
        author = next(search_query)
        list1.append(author)
        print(author)
    except:
        print("End of the iterator")
        break;
print(list1)
#
# # Print the titles of the author's publications
# print([pub.bib['title'] for pub in author.publications])
#
# # Take a closer look at the first publication
# pub = author.publications[0].fill()
# print(pub)
#
# # Which papers cited that publication?
# print([citation.bib['title'] for citation in pub.citedby])