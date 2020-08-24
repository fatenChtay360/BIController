import unittest
import json
import tornado.web
import tornado.testing
from tornado.testing import AsyncHTTPTestCase
import controller as cont  
from tornado import gen, httpclient, ioloop
import os
import pathlib

http_client = httpclient.AsyncHTTPClient()

class BaseHandler(AsyncHTTPTestCase):
    def get_app(self): 
        app = cont.app()
        return app

def open_json_file(file_path):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "testcases/{}".format(file_path))
    with open(filename) as f:
        data = json.load(f)
    return data

def http_request(url, method, body):
    request = httpclient.HTTPRequest(url, method= method, body=json.dumps(body))
    return request
