#!/usr/bin/python
import tornado.web
import tornado.ioloop
import requests
from requests.exceptions import HTTPError
import asyncio
from tornado.httpclient import AsyncHTTPClient


class RequestHandler(tornado.web.RequestHandler):
    pass
                                   
class CreateServiceHandler(RequestHandler):
    
    async def post(self):
        self.write("POST REQUEST")


class ModifyServiceHandler(RequestHandler):
    async def put(self, id):
        self.write("PUT REQUEST" + id)
     
    async def delete(self, id):
        self.write("DELETE REQUEST" + id)
        
class MWRServiceHandler(RequestHandler):
    def post(self, serviceID, MWRID):
        self.write(serviceID + " " + MWRID)

    def delete(self, serviceID, MWRID):
        pass
        
class CallBackServiceHandler(RequestHandler):
    def post(self):
       self.write("CALLBACK")

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/bi/mpls/v1/service", CreateServiceHandler),
        (r"/bi/mpls/v1/service/([0-9]+)", ModifyServiceHandler),
        (r"/bi/mpls/v1/service/([0-9]+)/mwr/([0-9]+)", MWRServiceHandler),
        (r"/client/listener", CallBackServiceHandler)
        
    ])
    app.listen(8881)
    print("I'm listening on port 8881")
    tornado.ioloop.IOLoop.current().start()

   
