#!/usr/bin/python
import tornado.web
import tornado.ioloop
import requests
from requests.exceptions import HTTPError
import json
import asyncio
from tornado.httpclient import AsyncHTTPClient
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import yaml
import jsonref

class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        with open("/BI.json") as f:
           schema = json.load(f)
        result = json.dumps(schema, sort_keys=False) 
        self.schema = jsonref.loads(result)


def check_conditions(path, json_data, value_to_be_checked = None):
    values = path.split('/')
    data = json_data
    try:
        for key in values:
            data = data[key]
    except:
        return False
    else:
        if (value_to_be_checked != None):
            if data == value_to_be_checked:
                return True
            else:
                return False
        else:
            return True
    
def validate_conditions(data):

    if data["serviceCharacteristic"][0]['value']['site']['management'] == 'customer-managed':
        newtork_access_type = "site-network-accesses"
    elif data["serviceCharacteristic"][0]['value']['site']['management'] == 'provider-managed':
        newtork_access_type = "telus-pe-ce-network-accesses"

    if check_conditions('value/site/management', data["serviceCharacteristic"][0], value_to_be_checked = "customer-managed") == True:
        if check_conditions('value/site/{}/site-network-access/telus-demarc-device-reference'.format(newtork_access_type), data["serviceCharacteristic"][0]) == True:
            print("yes")
        else: 
            print("no")

    elif check_conditions('value/site/management', data["serviceCharacteristic"][0], value_to_be_checked = "provider-managed") == True:
        if check_conditions('value/site/{}/site-network-access/telus-device-reference'.format(newtork_access_type), data["serviceCharacteristic"][0]) == True:
            print("yes")
        else: 
            print("no")

    if check_conditions('value/site/{}/site-network-access/bearer/requested-type/requested-type'.format(newtork_access_type), data["serviceCharacteristic"][0], value_to_be_checked= "HS" or "DSL") == True:
        if check_conditions('value/site/{}/site-network-access/bearer/telus-pe-tp-info'.format(newtork_access_type), data["serviceCharacteristic"][0]):
            print("yes")
        else: 
            print("no")

    if check_conditions("value/site/telus-ipv6-service", data["serviceCharacteristic"][0], value_to_be_checked = bool("true")) == True:
        if check_conditions('value/site/{}/site-network-access/bearer/requested-type/requested-type'.format(newtork_access_type), data["serviceCharacteristic"][0], value_to_be_checked= "HS" or "DSL") == True:
            print("yes")
        else: 
            print("no")

class CreateServiceHandler(RequestHandler):
    
    async def post(self):
        
        data=  json.loads(self.request.body.decode("UTF-8"))

        schema = self.schema["paths"]["/bi/mpls/v1/service"]["post"]["requestBody"]["content"]["application/json"]["schema"]

        try:
            validate(instance=data, schema=schema)
        except:
            self.write("ERRORRR- Return Response to NB- Status code -400")
        else:
            validate_conditions(data= data)
    
if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/bi/mpls/v1/service", CreateServiceHandler)
        
    ])
    app.listen(8881)
    print("I'm listening on port 8881")
    tornado.ioloop.IOLoop.current().start()

   
