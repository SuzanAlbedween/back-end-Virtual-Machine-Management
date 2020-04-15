import json
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS,cross_origin
import random
from Management import *
from DBuser import *
app = Flask(__name__)
CORS(app)
api = Api(app)


class VMDTO:

    def __init__(self,VMName,OperatingSystem, Status, Ram, Storage, LifeTime,iso,username,password,host):
        self.name=str(VMName)
        self.os=str(OperatingSystem)
        self.status=str(Status)
        self.ram=int(Ram)
        self.storage=int(Storage)
        self.lifetime=int(LifeTime)
        self.username=str(username)
        self.password=str(password)
        self.host=str(host)
        self.isopath=str(iso)

#class authentication:
#****************************
#data=[{"name":"suzi2","password":"12345"},{"name":"bibi","password":"92345"}]
class authentication(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")
        parser.add_argument("host")
        parser.add_argument("typesearch")
        params = parser.parse_args()
        obj=VMDTO(params["typesearch"],None,None,0,0,0,None,params["username"],params["password"],params["host"])
        if(obj.name!=None and obj.username!=None and obj.password!=None and obj.host!=None):
            print(obj.host,obj.username,obj.password,obj.name)
            res=GetAllVm(obj.host,obj.username,obj.password,obj.name)
            return str(res), 200
        else:
            print("missing arguments")
        return str(False), 400




    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("VMname")
        parser.add_argument("username")
        parser.add_argument("password")
        parser.add_argument("host")
        params = parser.parse_args()
        obj = VMDTO(params["VMname"],None,None,0,0,0,None,params["username"],params["pwd"],params["host"])
        if(obj.name!=None and obj.username!=None and obj.password!=None and obj.host!=None):
            print(obj.name,obj.username,obj.password,obj.host)
            res=DeleteVM(obj.name,obj.host,obj.username,obj.password)
            return str(res), 200
        else:
            print("missing arguments")
            return str(False),400
    def put(self):
        #username, password,vmname,newdate
        parser = reqparse.RequestParser()
        parser.add_argument("VMname")
        parser.add_argument("username")
        parser.add_argument("password")
        parser.add_argument("new date")
        params = parser.parse_args()
        obj=VMDTO(params["VMname"],None,None,0,0,0,None,params["username"],params["password"],None)
        print(obj.name,obj.username,obj.password,"new date=",params["new date"])
        if((obj.name==None) or (obj.username==None) or (obj.password==None) or (params["new date"]==None)):
            print("missing arguments")
            return str(False), 400
        else:
            res = ExtendVM(obj.username, obj.password, obj.name, params["new date"])
            return str(res), 200


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("VMname")
        parser.add_argument("OperatingSystem")
        parser.add_argument("Status")
        parser.add_argument("Ram")
        parser.add_argument("Storage")
        parser.add_argument("LifeTime")
        parser.add_argument("pathiso")
        parser.add_argument("username")
        parser.add_argument("password")
        parser.add_argument("host")
        params = parser.parse_args()
        obj=VMDTO(params["VMname"],params["OperatingSystem"],params["Status"],params["Ram"],params["Storage"],params["LifeTime"],params["pathiso"],params["username"],params["password"],params["host"])
        if(obj.name==None or obj.os==None or obj.status==None or obj.ram==None or obj.storage==None or obj.lifetime==None or obj.isopath==None or obj.username==None or obj.password==None or obj.host==None):
            print(" missing arguments")
            return 400
        else:
            print(params["VMname"],params["OperatingSystem"],params["Status"],params["Ram"]
                  ,params["Storage"],params["LifeTime"],params["pathiso"],params["username"],params["password"],params["host"])
            print("************obj*************************")
            print(obj.name, obj.os,obj.status,obj.ram,obj.storage,obj.lifetime,obj.isopath,obj.username,obj.password,obj.host)

            res = Create(obj.name,obj.os,obj.ram,obj.storage,obj.lifetime,obj.password,obj.username,obj.host,obj.isopath,obj.status)
            return str(res), 200


api.add_resource(authentication, "/VMM", "/VMM/", "/VMM/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
