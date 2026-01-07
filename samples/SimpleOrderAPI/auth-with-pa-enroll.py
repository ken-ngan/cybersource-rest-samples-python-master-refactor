import os
from importlib.machinery import SourceFileLoader

def auth_with_pa_enroll(referenceCode, currency, totalAmount, cardNumber, expMonth, expYear, cardType, city, country, email, phone, firstName, lastName, postalCode, address, referenceId, returnUrl):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_transaction = {}
    
    data_transaction['billTo_city'] = city
    data_transaction['billTo_country'] = country
    data_transaction['billTo_email'] = email
    data_transaction['billTo_phoneNumber'] = phone
    data_transaction['billTo_firstName'] = firstName
    data_transaction['billTo_lastName'] = lastName
    data_transaction['billTo_postalCode'] = postalCode
    data_transaction['billTo_street1'] = address
    
    data_transaction['card_accountNumber'] = cardNumber
    data_transaction['card_expirationMonth'] = expMonth
    data_transaction['card_expirationYear'] = expYear
    data_transaction['card_cardType'] = cardType
    
    data_transaction['ccAuthService_run'] = 'true'
    data_transaction['ccCaptureService_run'] = 'true'
    # data_transaction['ccAuthService_reconciliationID'] = referenceCode
    
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = referenceCode

    data_transaction['payerAuthEnrollService_referenceID'] = referenceId
    data_transaction['payerAuthEnrollService_returnURL'] = returnUrl
    data_transaction['payerAuthEnrollService_run'] = 'true'
    
    data_transaction['purchaseTotals_currency'] = currency
    data_transaction['purchaseTotals_grandTotalAmount'] = totalAmount

    print("\nAPI RESQUEST CODE : ", data_transaction)

    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    auth_with_pa_enroll("KN2024120404", "HKD", "10", "8100010000000142", "12", "2027", "062", "Mountain View", "HK", "jsmith@example.com", "35293565", "Jane", "Smith", "00000", "Charleston", 'f13fe5e0-9b47-4ea1-a03a-ec360f4d0f9f', 'https://example.com/step-up-return-url.jsp')
