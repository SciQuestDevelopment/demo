from flask import Flask
from flask_restful import Api,Resource,reqparse
from scholarly import scholarly
import json
# __name__ is the name of the module
app = Flask(__name__)
api = Api(app)

class auth(Resource):
    def get(self, author):
        search_query = scholarly.search_author(author)
        author = next(search_query)
        data = {'name': author.name, 'affilication': author.affiliation, 'email': author.email,
                'picture': author.url_picture,}
        jsonStr = json.dumps(data)
        # author.fill(sections=['publications'])
        return jsonStr

class pub(Resource):
    def get(self, pub):
        query = scholarly.search_pubs(pub)
        pub = next(query)
        jsonStr = json.dumps(pub.bib)
        return jsonStr

api.add_resource(auth,"/scholarly/author/<string:author>")
api.add_resource(pub,"/scholarly/pub/<string:pub>")

if __name__ == '__main__':
    app.run(debug=True)
