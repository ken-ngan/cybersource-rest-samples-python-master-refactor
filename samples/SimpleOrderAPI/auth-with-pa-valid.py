import os
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "utils.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

def auth_with_pa_valid(referenceCode, cardNumber, expMonth, expYear, cardType, currency, totalAmount, firstName, lastName, address, city, postalCode, country, email, phone, transaction_id):
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
    
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = referenceCode
    # data_transaction['ccAuthService_reconciliationID'] = "1234567890"

    data_transaction['payerAuthValidateService_authenticationTransactionID'] = transaction_id
    data_transaction['payerAuthValidateService_run'] = 'true'
    
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
    auth_with_pa_valid("TC50171_3", "4000000000001091", "01", "2023", "001", "HKD",  "30.00", "John", "Smith", "201 S. Division St._1", "Foster City", "00000", "HK", "accept@cybs.com", "6504327113", "OiCtXA1j1AxtSNDh5lt1")
