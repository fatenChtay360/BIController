#!/usr/bin/python
import tornado.web
import tornado.ioloop
import requests
import json
import asyncio
from tornado.httpclient import AsyncHTTPClient
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import yaml
import jsonref
import payload_validation as val
import uuid
import os

operation_accepted_response = {
  "requestId": str(uuid.uuid4())
}

operation_failed_response = {
  "status": "error",
  "reason": "Input Validation Failed",
  "code": "ERR001"
}

class RequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "/home/saugo/Desktop/ControlCode/test/controller/openapi.yaml")
        with open(filename) as f:
           schema = yaml.safe_load(f)
        result = json.dumps(schema, sort_keys=False) 
        openapi_schema = jsonref.loads(result)

        self.BIServiceTMF_schema = openapi_schema["components"]["schemas"]["BIServiceTMF"]
        self.CallBack_schema = openapi_schema["components"]["schemas"]["CallBack"]
        self.request_payload = json.loads(self.request.body.decode("UTF-8"))
    
class ResponseToNB(RequestHandler):
    def validate_request_payload(self, request_payload, openapi_schema, validate_conditions= False):
        try:
                validate(instance=request_payload, schema= openapi_schema)
        except:
                self.write(operation_failed_response)
        else:
            if(validate_conditions != False):
                if (val.validate_customer_managed(request_payload) and val.validate_provider_managed(request_payload) and val.validate_telus_ipv6_service(request_payload) 
                    and val.validate_telus_access_type(request_payload) and val.validate_requested_type(request_payload) and val.validate_encapsulation(request_payload)):  
                    self.write(operation_accepted_response) 
                else:
                    self.write(operation_failed_response)
            else:
                self.write(operation_accepted_response) 
     
class CreateServiceHandler(RequestHandler):
    async def post(self):
        create_service_schema = self.BIServiceTMF_schema
        ResponseToNB.validate_request_payload(self, self.request_payload, create_service_schema, validate_conditions= True)
        
class ModifyServiceHandler(RequestHandler):
    async def put(self, id):
        update_service_schema = self.BIServiceTMF_schema
        ResponseToNB.validate_request_payload(self, self.request_payload, update_service_schema, validate_conditions= True)
         
    async def delete(self, id):
        pass
    
class ActivatePortHandler(RequestHandler):
    async def put(self, id):
        pass

class MWRServiceHandler(RequestHandler):
    async def post(self, serviceID, MWRID):
        wireless_resiliency_schema = self.BIServiceTMF_schema
        ResponseToNB.validate_request_payload(self, self.request_payload, wireless_resiliency_schema, validate_conditions= True)

    async def delete(self, serviceID, MWRID):
        pass
        
class CallBackServiceHandler(RequestHandler):
    async def post(self):
        callbacktoNB_schema = self.CallBack_schema
        ResponseToNB.validate_request_payload(self, self.request_payload, callbacktoNB_schema)
       
class PortalRequestHandler(RequestHandler):
    async def get(self):
        pass
    
def app():
    app = tornado.web.Application([
        (r"/bi/mpls/v1/service", CreateServiceHandler),
        (r"/bi/mpls/v1/service/([0-9]+)", ModifyServiceHandler),
        (r'/bi/mpls/v1/service/{id}/activate', ActivatePortHandler),
        (r"/bi/mpls/v1/service/([0-9]+)/mwr/([0-9]+)", MWRServiceHandler),
        (r"/client/listener", CallBackServiceHandler),
        (r'/bi/mpls/v1/requests', PortalRequestHandler),
    ])
    return app

if __name__ == "__main__":
    app = app()
    app.listen(8881)
    print("I'm listening on port 8881")
    tornado.ioloop.IOLoop.current().start()

   
