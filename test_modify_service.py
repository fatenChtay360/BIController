from test_base_class import *
import test_base_class as base

ModifyServiceURL = "http://localhost:8881/bi/mpls/v1/service/1"

class ModifyServiceTest(base.BaseHandler):

    @tornado.testing.gen_test
    def test_create_valid_request_one(self): 
        valid_data = base.open_json_file('create_valid.json')
        request = base.http_request(ModifyServiceURL, method="PUT", body= valid_data)
        response = yield base.http_client.fetch(request)
        self.assertIn("requestId", response.body.decode())

    @tornado.testing.gen_test
    def test_create_nonvalid_request(self): #changed management to a value that is not among enums
        non_valid_data = base.open_json_file('create_nonvalid.json')
        request = base.httpclient.HTTPRequest(ModifyServiceURL, method="PUT", body= json.dumps(non_valid_data))
        response = yield base.http_client.fetch(request)
        self.assertIn("error", response.body.decode())

if __name__ == '__main__':
    unittest.main()