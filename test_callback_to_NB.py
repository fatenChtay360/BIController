from test_base_class import *
import test_base_class as base

CallBackURL = "http://localhost:8881/client/listener"

class CallBackTestCase(base.BaseHandler):
    @tornado.testing.gen_test
    def test_valid_callback(self):
        valid_callback_data = base.open_json_file("callback_valid.json")
        request = base.http_request(CallBackURL, method="POST", body= valid_callback_data)
        response = yield http_client.fetch(request)
        self.assertIn("requestId", response.body.decode())

    @tornado.testing.gen_test
    def test_non_valid_callback(self):
        non_valid_callback_data = base.open_json_file("callback_nonvalid.json")
        request = base.http_request(CallBackURL, method="POST", body= non_valid_callback_data)
        response = yield http_client.fetch(request)
        self.assertIn("error", response.body.decode())

if __name__ == '__main__':
    unittest.main()