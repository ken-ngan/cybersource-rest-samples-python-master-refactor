import os
from importlib.machinery import SourceFileLoader

def retrieve_token(referenceCode, savedtoken):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_merchant = {'merchantID': merchant_id}
    data_order = {}
    data_order['merchantReferenceCode'] = referenceCode
    data_order['recurringSubscriptionInfo_subscriptionID'] = savedtoken
    data_order['paySubscriptionRetrieveService_run'] = 'true'

    data_transaction = {**data_merchant, **data_order}
    
    print("\nAPI RESQUEST CODE : ", data_transaction)

    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    retrieve_token('KN25032104', '7416706729026417503979')