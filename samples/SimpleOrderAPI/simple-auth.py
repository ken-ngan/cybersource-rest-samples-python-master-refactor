import os
from importlib.machinery import SourceFileLoader

def simple_auth(**kwargs):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    # Initialize client
    client = configuration.CyberSourceClient(
        configuration.SOAP_WSDL,
        configuration.SOAP_P12_FILE,
        configuration.SOAP_P12_PASSWORD
    )

    # Build transaction data with defaults
    data_transaction = {
        'merchantID': configuration.SOAP_USERNAME,
        'ccAuthService_run': 'true',
        'ccCaptureService_run': 'true',
        'ccAuthService_commerceIndicator': 'internet',
        'purchaseTotals_currency': 'HKD',
        'purchaseTotals_grandTotalAmount': '1',
        **kwargs
    }

    print("\nAPI REQUEST DATA:", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except KeyError:
        print('Request ID does not exist.')

if __name__ == '__main__':
    payment_data = {
        'merchantReferenceCode': 'KN250707C',
        'ccAuthService_reconciliationID': 'KN250707C',
        'card_accountNumber': '5289311000000002',
        'card_expirationMonth': '12',
        'card_expirationYear': '2027',
        'card_cardType': '002',
        'billTo_firstName': 'Ken',
        'billTo_lastName': 'Ngan',
        'billTo_street1': '27F Manhattan Place',
        'billTo_city': 'Kowloon Bay',
        'billTo_postalCode': '00000',
        'billTo_country': 'HK',
        'billTo_email': 'ken@example.com',
        'billTo_phoneNumber': '91360955'
    }
    simple_auth(**payment_data)