management_path = "value/site/management"
entries_path ="value/site/vpn-policies/vpn-policy/mpls-bi/entries"
telus_ipv6_service_path = "value/site/telus-ipv6-service"
vpnpolicy_path = "value/site/vpn-policies"
request_type= "site-network-access/bearer/requested-type/requested-type"
telus_pe_tp_info_path= "site-network-access/bearer/telus-pe-tp-info"

def check_conditions(parameter_path, payload_data, value_to_be_checked = None):
    parameter = parameter_path.split('/')
    data = payload_data
    try:
        for value in parameter:
            data = data[value]
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

def get_network_access_type(request_payload):
    managed_path= request_payload["serviceCharacteristic"][0]['value']['site']['management']
    if managed_path == 'customer-managed':
        network_access_type = "site-network-accesses"
    elif managed_path == 'provider-managed':
        network_access_type = "telus-pe-ce-network-accesses"
    return network_access_type

def validate_telus_access_type(request_payload):
    telus_device_loopback_path = "value/site/{}/site-network-access/telus-device-loopback-address".format(get_network_access_type(request_payload))
    site_network_access_type_path = "value/site/{}/site-network-access/site-network-access-type".format(get_network_access_type(request_payload))
    # print(site_network_access_type_path)
    if check_conditions(site_network_access_type_path, request_payload["serviceCharacteristic"][0], value_to_be_checked= "telus-re-direct"):
        if (check_conditions(vpnpolicy_path, request_payload["serviceCharacteristic"][0])) and (check_conditions("{}/customer-prefixes".format(entries_path), request_payload["serviceCharacteristic"][0]) or check_conditions("{}/telus-provider-prefixes".format(entries_path), request_payload["serviceCharacteristic"][0])):
            return True
        else:
            return False

    elif check_conditions(site_network_access_type_path, request_payload["serviceCharacteristic"][0], value_to_be_checked= "telus-mwr"):
        if check_conditions(telus_device_loopback_path, request_payload["serviceCharacteristic"][0]):
            return True
        else:
            return False

def validate_customer_managed(request_payload):
    if check_conditions(management_path, request_payload["serviceCharacteristic"][0], value_to_be_checked = "customer-managed"):
        #Not sure about the second one 
        if check_conditions('value/site/{}/site-network-access/telus-demarc-device-reference'.format(get_network_access_type(request_payload)), request_payload["serviceCharacteristic"][0]) and check_conditions('value/site/telus-demarc-devices', request_payload["serviceCharacteristic"][0]):
           return True
        else: 
            return False
    else:
        return True

def validate_provider_managed(request_payload):

    if check_conditions(management_path, request_payload["serviceCharacteristic"][0], value_to_be_checked = "provider-managed"):
        if check_conditions('value/site/{}/site-network-access/telus-device-reference'.format(get_network_access_type(request_payload)), request_payload["serviceCharacteristic"][0]) and check_conditions('value/site/devices', request_payload["serviceCharacteristic"][0]):
            return True
        else: 
            return False
    else:
        return True

def validate_requested_type(request_payload):
    request_type_path = "value/site/{}/{}".format(get_network_access_type(request_payload), request_type)
    if check_conditions(request_type_path, request_payload["serviceCharacteristic"][0], value_to_be_checked= "HS" or "DSL"):
        if check_conditions('value/site/{}/{}'.format(get_network_access_type(request_payload), telus_pe_tp_info_path), request_payload["serviceCharacteristic"][0]):
             return True
        else: 
            return False
    else:
        return True

def validate_telus_ipv6_service(request_payload):
    request_type_path = "value/site/{}/{}".format(get_network_access_type(request_payload), request_type)
    ipv6_path = "value/site/{}/site-network-access/ip-connection/ipv6".format(get_network_access_type(request_payload))

    if check_conditions(telus_ipv6_service_path, request_payload["serviceCharacteristic"][0], value_to_be_checked = bool("true")) and check_conditions(request_type_path, request_payload["serviceCharacteristic"][0], value_to_be_checked= "HS" or "DSL"):
        if check_conditions(ipv6_path, request_payload["serviceCharacteristic"][0]):
            return True 
        else:
            return False 
    else:
        return True


def validate_encapsulation(request_payload):
    encapsulation_path= "value/site/{}/{}/encapsulation".format( get_network_access_type(request_payload), telus_pe_tp_info_path)
    vlan_inner_id= "value/site/{}/{}/vlan-inner-id".format(get_network_access_type(request_payload), telus_pe_tp_info_path)
    vlan_id= "value/site/{}/{}/vlan-id".format(get_network_access_type(request_payload), telus_pe_tp_info_path)

    if check_conditions(encapsulation_path, request_payload["serviceCharacteristic"][0], value_to_be_checked = "qinq"):
        if check_conditions(vlan_inner_id, request_payload["serviceCharacteristic"][0]):
            return True 
        else:
            return False 
    else:
        return True

    if check_conditions(encapsulation_path, request_payload["serviceCharacteristic"][0], value_to_be_checked = "qinq" or "dot1q"):
        if check_conditions(vlan_id, request_payload["serviceCharacteristic"][0]):
            return True 
        else:
            return False 
    else:
        return True


