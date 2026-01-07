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

def authorization_with_customer_token_default_payment_instrument_and_shipping_address_creation(referenceInfoCode, cardNumber, expMonth, expYear, cvv, cardType, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phone, stFirstName, stLastName, stAddress, stLocality, stPostalCode, stCountry):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )


    processingInformationActionList = []
    processingInformationActionList.append("TOKEN_CREATE")

    processingInformationActionTokenTypes = []
    processingInformationActionTokenTypes.append("customer")
    processingInformationActionTokenTypes.append("paymentInstrument")
    processingInformationActionTokenTypes.append("shippingAddress")
    processingInformationCapture = False
    processingInformation = Ptsv2paymentsProcessingInformation(
        action_list = processingInformationActionList,
        action_token_types = processingInformationActionTokenTypes,
        capture = processingInformationCapture
    )

    paymentInformationCardNumber = cardNumber
    paymentInformationCardExpirationMonth = expMonth
    paymentInformationCardExpirationYear = expYear
    paymentInformationCardSecurityCode = cvv
    paymentInformationCardType = cardType
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        number = paymentInformationCardNumber,
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear,
        security_code = paymentInformationCardSecurityCode,
        type = paymentInformationCardType
    )

    # paymentInformationCustomerId = "AB695DA801DD1BB6E05341588E0A3BDC"
    # paymentInformationCustomer = Ptsv2paymentsPaymentInformationCustomer(
    #     id = paymentInformationCustomerId
    # )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        card = paymentInformationCard.__dict__,
    #     customer = paymentInformationCustomer.__dict__
    )

    orderInformationAmountDetailsTotalAmount = totalAmount
    orderInformationAmountDetailsCurrency = currency
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformationBillToFirstName = firstName
    orderInformationBillToLastName = lastName
    orderInformationBillToAddress1 = address
    orderInformationBillToLocality = locality
    orderInformationBillToPostalCode = postalCode
    orderInformationBillToCountry = country
    orderInformationBillToEmail = email
    orderInformationBillToPhoneNumber = phone
    orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
        first_name = orderInformationBillToFirstName,
        last_name = orderInformationBillToLastName,
        address1 = orderInformationBillToAddress1,
        locality = orderInformationBillToLocality,
        postal_code = orderInformationBillToPostalCode,
        country = orderInformationBillToCountry,
        email = orderInformationBillToEmail,
        phone_number = orderInformationBillToPhoneNumber
    )

    orderInformationShipToFirstName = stFirstName
    orderInformationShipToLastName = stLastName
    orderInformationShipToAddress1 = stAddress
    orderInformationShipToLocality = stLocality
    orderInformationShipToPostalCode = stPostalCode
    orderInformationShipToCountry = stCountry
    orderInformationShipTo = Ptsv2paymentsOrderInformationShipTo(
        first_name = orderInformationShipToFirstName,
        last_name = orderInformationShipToLastName,
        address1 = orderInformationShipToAddress1,
        locality = orderInformationShipToLocality,
        postal_code = orderInformationShipToPostalCode,
        country = orderInformationShipToCountry
    )

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__,
        bill_to = orderInformationBillTo.__dict__,
        ship_to = orderInformationShipTo.__dict__
    )

    tokenInformationPaymentInstrument_default = True
    tokenInformationPaymentInstrument = Ptsv2paymentsTokenInformationPaymentInstrument(
        default = tokenInformationPaymentInstrument_default
    )

    tokenInformationShippingAddress_default = True
    tokenInformationShippingAddress = Ptsv2paymentsTokenInformationShippingAddress(
        default = tokenInformationShippingAddress_default
    )

    tokenInformation = Ptsv2paymentsTokenInformation(
        payment_instrument = tokenInformationPaymentInstrument.__dict__,
        shipping_address = tokenInformationShippingAddress.__dict__
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__,
        token_information = tokenInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)
    
    print("\nAPI REQUEST CODE 456 : ", requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        return_data, status, body = api_instance.create_payment(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    authorization_with_customer_token_default_payment_instrument_and_shipping_address_creation("TC5012345", "4111111111111111", "12", "2031", "123", "001", "0", "HKD", "John", "Doe", "1 Market St", "san francisco", "00000", "HK", "test@cybs.com", "4158880000", "John", "Doe", "1 Market St", "san francisco", "00000", "HK")
