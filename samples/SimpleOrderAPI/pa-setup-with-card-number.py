import os
from importlib.machinery import SourceFileLoader

def pa_setup_with_card_number(cardNumber, expMonth, expYear):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_transaction = {}    
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = 'cybs_test'
    data_transaction['card_accountNumber'] = cardNumber
    data_transaction['card_expirationMonth'] = expMonth
    data_transaction['card_expirationYear'] = expYear
    data_transaction['payerAuthSetupService_run'] = 'true'
    
    print("\nAPI RESQUEST CODE : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    pa_setup_with_card_number("5289460006139437", "12", "2027")