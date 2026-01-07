from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.plugins import HistoryPlugin
from lxml import etree
import os
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "utils.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

def mpgs_authorization_with_google_pay(referenceCode, firstName, lastName, address, locality, postalCode, country, email, googlePayBlob, currency, totalAmount):
    wsdl = configuration.SOAP_WSDL
    username = configuration.SOAP_USERNAME
    password = configuration.SOAP_PASSWORD
    history = HistoryPlugin()
    client = Client(wsdl, wsse=UsernameToken(username, password), plugins=[history])
    client.set_ns_prefix(None,'urn:schemas-cybersource-com:transaction-data-1.161') #To remove the ns0 namespace

    self_filename = os.path.basename(__file__)[:-3] #remove extension

    data_transaction = {}
    data_transaction['merchantID'] = username
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

    result = configuration.send_request(client, data_transaction)
    configuration.show_result(result)
    try:
        filename = result['requestID']
        decision = result['decision']
        os.makedirs(self_filename, exist_ok=True)
        with open(f'{self_filename}/{decision}-{filename}.txt', 'w') as file:
            for hist in [history.last_sent, history.last_received]:
                file.write(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
                file.write('--------------------------------\r\n')
    except (KeyError):
        print('Request ID is not exist.')
    return result

if __name__ == '__main__':
    mpgs_authorization_with_google_pay("test_google_pay", "Ken", "Ngan", "27/F, Manhattan Place", "Kowloon Bay", "00000", "HK", "ken.ngan@globalpay.com", "googlePayBlob", "HKD", "123")