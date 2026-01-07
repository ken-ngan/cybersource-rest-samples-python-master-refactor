import traceback
import os
from importlib.machinery import SourceFileLoader

def auth_with_pa_enroll_and_cus_token_creation(city, country, email, phone, firstName, lastName, postalCode, address, cardType, cardNumber, expMonth, expYear, currency, totalAmount, referenceCode, referenceId, returnUrl):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.SOAP_WSDL
    p12_file = configuration.SOAP_P12_FILE
    p12_password = configuration.SOAP_P12_PASSWORD
    merchant_id = configuration.SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)
    
    data_billing = {}
    data_billing['billTo_city'] = city
    data_billing['billTo_country'] = country
    data_billing['billTo_email'] = email
    data_billing['billTo_phoneNumber'] = phone
    data_billing['billTo_firstName'] = firstName
    data_billing['billTo_lastName'] = lastName
    data_billing['billTo_postalCode'] = postalCode
    data_billing['billTo_street1'] = address
    
    data_card = {}
    data_card['card_cardType'] = cardType
    data_card['card_accountNumber'] = cardNumber
    data_card['card_expirationMonth'] = expMonth
    data_card['card_expirationYear'] = expYear

    data_merchant = {}
    data_merchant['merchantID'] = merchant_id
    
    data_order = {}
    data_order['paySubscriptionCreateService_run'] = 'true'
    data_order['recurringSubscriptionInfo_frequency'] = 'on-demand'
    data_order['ccAuthService_run'] = 'true'
    data_order['ccCaptuService_run'] = 'true'
    data_order['payerAuthEnrollService_referenceID'] = referenceId
    data_order['payerAuthEnrollService_returnURL'] = returnUrl
    data_order['payerAuthEnrollService_run'] = 'true'
    data_order['purchaseTotals_currency'] = currency
    data_order['purchaseTotals_grandTotalAmount'] = totalAmount
    data_order['merchantReferenceCode'] = referenceCode
    data_order['subsequentAuthFirst'] = 'true'
    data_order['payerAuthEnrollService_challengeCode'] = '04'
    data_order['firstRecurringPayment'] = 'true'

    data_transaction = {**data_billing, **data_card, **data_merchant, **data_order}
    
    print("\nAPI RESQUEST CODE : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        configuration.show_result(result)
        return result
    except KeyboardInterrupt:
        exit()
    except Exception:
        traceback.print_exc()
        raise

if __name__ == '__main__':
    auth_with_pa_enroll_and_cus_token_creation('Kownloon', 'HK', 'zen@iamzen.info', '35293567', 'Zen', 'Chiu', '00000', 'KLN', '001', '4111111111111111', '05', '23', 'HKD', '100', 'refnum1234', 'f13fe5e0-9b47-4ea1-a03a-ec360f4d0f9f', 'https://example.com/step-up-return-url.jsp')
