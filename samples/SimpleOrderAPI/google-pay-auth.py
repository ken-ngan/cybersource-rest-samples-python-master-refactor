import os
from importlib.machinery import SourceFileLoader

def google_pay_auth(referenceCode, firstName, lastName, address, locality, postalCode, country, email, googlePayBlob, currency, totalAmount):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_transaction = {}
    data_transaction['merchantID'] = merchant_id
    data_transaction['ccAuthService_run'] = 'true'
    data_transaction['ccCaptureService_run'] = 'true'
    data_transaction['merchantReferenceCode'] = referenceCode
    data_transaction['ccAuthService_reconciliationID'] = referenceCode
    data_transaction['billTo_firstName'] = firstName
    data_transaction['billTo_lastName'] = lastName
    data_transaction['billTo_street1'] = address
    data_transaction['billTo_city'] = locality
    data_transaction['billTo_postalCode'] = postalCode
    data_transaction['billTo_country'] = country
    data_transaction['billTo_email'] = email
    data_transaction['paymentSolution'] = '012'
    data_transaction['encryptedPayment_data'] = googlePayBlob
    data_transaction['purchaseTotals_currency'] = currency
    data_transaction['purchaseTotals_grandTotalAmount'] = totalAmount

    print("\n----- samples/SimpleOrderAPI/google-pay-auth.py -----")
    print("\nAPI REQUEST BODY : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    google_pay_auth("test_google_pay", "Ken", "Ngan", "27/F, Manhattan Place", "Kowloon Bay", "00000", "HK", "ken.ngan@globalpay.com", "googlePayBlob", "HKD", "123")