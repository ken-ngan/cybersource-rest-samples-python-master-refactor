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

def auth_with_pa_enroll_and_pi_token(referenceInfoCode, paymentInstrumentId, expMonth, expYear, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phone, returnUrl, referenceId):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    processingInformationActionList = []
    processingInformationActionList.append("CONSUMER_AUTHENTICATION")
    processingInformationCapture = False
    processingInformation = Ptsv2paymentsProcessingInformation(
        action_list = processingInformationActionList,
        capture = processingInformationCapture
    )

    paymentInformationCardExpirationMonth = expMonth
    paymentInformationCardExpirationYear = expYear
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear
    )

    paymentInformationPaymentInstrumentId = paymentInstrumentId
    paymentInformationPaymentInstrument = Ptsv2paymentsPaymentInformationPaymentInstrument(
        id = paymentInformationPaymentInstrumentId
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        # card = paymentInformationCard.__dict__,
        payment_instrument = paymentInformationPaymentInstrument.__dict__
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

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__,
        bill_to = orderInformationBillTo.__dict__
    )

    consumerAuthenticationInformationMessageCategory = None
    if totalAmount == "0.00":
        consumerAuthenticationInformationMessageCategory = '02'

    consumerAuthenticationInformationReturnURL = returnUrl
    consumerAuthenticationInformationReferenceId = referenceId
    consumerAuthenticationInformation = Ptsv2paymentsConsumerAuthenticationInformation(
        message_category=consumerAuthenticationInformationMessageCategory,
        return_url = consumerAuthenticationInformationReturnURL,
        reference_id = consumerAuthenticationInformationReferenceId
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__,
        consumer_authentication_information = consumerAuthenticationInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\n----- samples/Payments/Payments/auth-with-pi-token-and-pa-enroll.py -----")
    print("\nAPI REQUEST CODE : ", requestObj)

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
    auth_with_pa_enroll_and_pi_token("TC50171_3", "FE39A95B0BDC3DF2E053AF598E0A0D57", "12", "2031", "102.21", "USD", "John", "Doe", "1 Market St", "san franciso", "00000", "HK", "test@cybs.com", "4158880000", "http://127.0.0.1:8000/views/token", "1591f14f-f862-4c6f-9bce-61057df03ed9")
