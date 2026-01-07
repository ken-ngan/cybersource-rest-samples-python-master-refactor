import os
from importlib.machinery import SourceFileLoader

def capture_payment(referenceCode, currency, totalAmount, id):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_transaction = {}

    data_transaction['ccCaptureService_authRequestID'] = id
    data_transaction['ccCaptureService_run'] = 'true'
    
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = referenceCode
    
    data_transaction['purchaseTotals_currency'] = currency
    data_transaction['purchaseTotals_grandTotalAmount'] = totalAmount
    
    print("\nAPI REQUEST BODY : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    capture_payment("TC50171_3", "HKD", "10", "7440763973276134004503")
