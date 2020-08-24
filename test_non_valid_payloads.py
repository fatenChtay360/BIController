from test_base_class import *
import test_base_class as test
from tornado import gen, httpclient, ioloop
import payload_validation as val


def assert_non_valid_data(self, json_data, function):
    validation = function(json_data)
    self.assertFalse(validation)

def assert_valid_data(self, json_data, function):
    validation = function(json_data)
    self.assertTrue(validation)

class ValidationTestCase(test.BaseHandler):

    @tornado.testing.gen_test
    def test_valid_re_direct(self): 
        valid_re_direct_data = test.open_json_file("create_valid.json")       
        assert_valid_data(self, valid_re_direct_data, val.validate_telus_access_type)
   
    @tornado.testing.gen_test
    def test_re_direct_without_vpnpolicy(self): 
        missing_vpn_policy = test.open_json_file("telus_re_direct_no_vpnpolicy.json")       
        assert_non_valid_data(self, missing_vpn_policy, val.validate_telus_access_type)

    @tornado.testing.gen_test
    def test_re_direct_with_vpnpolicy(self): 
        vpn_policy = test.open_json_file("create_valid.json")       
        assert_valid_data(self, vpn_policy, val.validate_telus_access_type)

    @tornado.testing.gen_test
    def test_mwr_without_loopback(self): 
        missing_loopback = test.open_json_file("telus_mwr_no_loopback.json")       
        assert_non_valid_data(self, missing_loopback, val.validate_telus_access_type)

    @tornado.testing.gen_test
    def test_mwr_with_loopback(self): 
        loopback = test.open_json_file("create_valid.json")       
        assert_valid_data(self, loopback, val.validate_telus_access_type)

    @tornado.testing.gen_test
    def test_customer_without_demarc_reference_and_devices(self): 
        missing_demarc_info = test.open_json_file("customer_managed_no_demarc_devices_and_reference.json")       
        assert_non_valid_data(self, missing_demarc_info, val.validate_customer_managed)

    @tornado.testing.gen_test
    def test_customer_with_demarc_reference_and_devices(self): 
        demarc_info = test.open_json_file("create_valid.json")       
        assert_valid_data(self, demarc_info, val.validate_customer_managed)

    @tornado.testing.gen_test
    def test_provider_without_reference_and_devices(self): 
        missing_reference_and_devices = test.open_json_file("provider_managed_no_devices_and_reference.json")       
        assert_non_valid_data(self, missing_reference_and_devices, val.validate_provider_managed)

    @tornado.testing.gen_test
    def test_provider_with_reference_and_devices(self): 
        reference_and_devices = test.open_json_file("create_valid.json")       
        assert_valid_data(self, reference_and_devices, val.validate_provider_managed)

    @tornado.testing.gen_test
    def test_request_type_HSorDSL_without_pe_tp_info(self): 
        missing_pe_tp_info = test.open_json_file("request_type_no_telus-pe-tp-info.json")       
        assert_non_valid_data(self, missing_pe_tp_info, val.validate_requested_type)

    @tornado.testing.gen_test
    def test_request_type_HSorDSL_with_pe_tp_info(self): 
        pe_tp_info = test.open_json_file("create_valid.json")       
        assert_valid_data(self, pe_tp_info, val.validate_requested_type)

    @tornado.testing.gen_test
    def test_ipv6_service_without_ipv6(self): 
        missing_ipv6 = test.open_json_file("ipv6service_no_ipv6.json")       
        assert_non_valid_data(self, missing_ipv6, val.validate_telus_ipv6_service)
    
    @tornado.testing.gen_test
    def test_ipv6_service_with_ipv6(self): 
        ipv6 = test.open_json_file("create_valid.json")       
        assert_valid_data(self,ipv6, val.validate_telus_ipv6_service)
        
    @tornado.testing.gen_test
    def test_encapsulation_without_vlan(self): 
        missing_vlan = test.open_json_file("encapsulation_no_vlan.json")       
        assert_non_valid_data(self, missing_vlan, val.validate_encapsulation)

    @tornado.testing.gen_test
    def test_encapsulation_with_vlan(self): 
        vlan = test.open_json_file("create_valid.json")       
        assert_valid_data(self, vlan, val.validate_encapsulation)

    # @tornado.testing.gen_test
    # def test_encapsulation_without_vlan_inner_id(self): 
    #     missing_vlan_id = test.open_json_file("encapsulation_no_vlan_inner_id.json")       
    #     assert_non_valid_data(self, missing_vlan_id, val.validate_encapsulation)
    
if __name__ == '__main__':
    unittest.main()
