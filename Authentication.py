from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource, reqparse
from flask.views import MethodView

from DBuser import *

app = Flask(__name__)
CORS(app)
api = Api(app )



class userDTO:

    def __init__(self,ID,username,userpassword):
        self.ID=ID
        self.username=str(username)
        self.userpassword=str(userpassword)


class authentication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("password")
        params = parser.parse_args()
        obj=userDTO(None,params["name"],params["password"])
        if((obj.username==None)or(obj.userpassword==None)):
            print(" missing arguments")
            return 400
        else:
            print(params["name"], params["password"])
            print("the obj is", obj.username, "  ", obj.userpassword)
            res = CheckLogIn(obj.username, obj.userpassword)
            return str(res), 200


api.add_resource(authentication, "/auth", "/auth/", "/auth/<string:name>")

if __name__ == '__main__':
    app.run(debug=True)
