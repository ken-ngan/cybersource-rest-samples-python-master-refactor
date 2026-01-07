import os
from importlib.machinery import SourceFileLoader

def delete_token(referenceCode, savedtoken):
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
    data_order['paySubscriptionDeleteService_run'] = 'true'

    data_transaction = {**data_merchant, **data_order}
    print("\nAPI REQUEST BODY : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    delete_token('Token-delete-4', '3424E4FAF11FF112E0631E588D0AC1EB')