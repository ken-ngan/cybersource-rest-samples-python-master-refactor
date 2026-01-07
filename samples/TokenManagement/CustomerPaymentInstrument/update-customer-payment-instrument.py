from CyberSource import *
from pathlib import Path
import os
import json
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def update_customer_payment_instrument():
    customerTokenId = "300B23C14371B012E0631E588D0AD8A0"
    paymentInstrumentTokenId = "7416706729026417503979"
    
    _default =  True
    
    cardExpirationMonth = "0"
    cardExpirationYear = "0"
    # cardType = "001"
    card = Tmsv2customersEmbeddedDefaultPaymentInstrumentCard(
        expiration_month = cardExpirationMonth,
        expiration_year = cardExpirationYear
        # type = cardType
    )

    # billToFirstName = "Ken"
    # billToLastName = "Ngan"
    # billToCompany = "Global Payments"
    # billToAddress1 = "1 Market St"
    # billToLocality = "San Francisco"
    # billToAdministrativeArea = "CA"
    # billToPostalCode = "94105"
    # billToCountry = "US"
    # billToEmail = "test@cybs.com"
    # billToPhoneNumber = "4158880000"
    # billTo = Tmsv2customersEmbeddedDefaultPaymentInstrumentBillTo(
    #     first_name = billToFirstName,
    #     last_name = billToLastName,
    #     company = billToCompany,
    #     address1 = billToAddress1,
    #     locality = billToLocality,
    #     administrative_area = billToAdministrativeArea,
    #     postal_code = billToPostalCode,
    #     country = billToCountry,
    #     email = billToEmail,
    #     phone_number = billToPhoneNumber
    # )

    # instrumentIdentifierId = "7030000000049977465"
    # instrumentIdentifier = Tmsv2customersEmbeddedDefaultPaymentInstrumentInstrumentIdentifier(
    #     id = instrumentIdentifierId
    # )

    requestObj = PatchCustomerPaymentInstrumentRequest(
        default = _default,
        # bill_to = billTo.__dict__,
        # instrument_identifier = instrumentIdentifier.__dict__,
        card = card.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\n----- samples/TokenManagement/CustomerPaymentInstrument/update-customer-payment-instrument.py -----")
    print("\nAPI REQUEST CODE : ", requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = CustomerPaymentInstrumentApi(client_config)
        return_data, status, body = api_instance.patch_customers_payment_instrument(customerTokenId, paymentInstrumentTokenId, requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling CustomerPaymentInstrumentApi->patch_customers_payment_instrument: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    update_customer_payment_instrument()
