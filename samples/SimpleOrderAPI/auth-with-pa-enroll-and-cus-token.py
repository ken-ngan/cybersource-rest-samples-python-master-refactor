import os
from importlib.machinery import SourceFileLoader

def auth_with_pa_enroll_and_cus_token(referenceCode, merchantDescriptor, currency, totalAmount, savedtoken, referenceId, returnUrl):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_transaction = {}
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = referenceCode
    data_transaction['invoiceHeader_merchantDescriptor'] = merchantDescriptor
    data_transaction['purchaseTotals_currency'] = currency
    data_transaction['purchaseTotals_grandTotalAmount'] = totalAmount
    data_transaction['recurringSubscriptionInfo_subscriptionID'] = savedtoken
    # data_transaction['card_expirationMonth'] = '06'
    # data_transaction['card_expirationYear'] = '2024'
    # data_transaction['card_cardType'] = "062"
    
    data_transaction['subsequentAuth'] = 'true'
    data_transaction['subsequentAuthTransactionID'] = ''
    data_transaction['ccAuthService_run'] = 'true'
    
    data_transaction['payerAuthEnrollService_referenceID'] = referenceId
    data_transaction['payerAuthEnrollService_returnURL'] = returnUrl
    data_transaction['payerAuthEnrollService_run'] = 'true'
    
    print("\nAPI RESQUEST CODE : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

if __name__ == '__main__':
    auth_with_pa_enroll_and_cus_token('cybs_test', 'authorization-with-token','HKD','100','FFA103423E1EAC7FE053A2598D0A4303', 'f13fe5e0-9b47-4ea1-a03a-ec360f4d0f9f', 'https://example.com/step-up-return-url.jsp')
