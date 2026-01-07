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

def rest_auth_with_pa_valid(referenceInfoCode, cardNumber, expMonth, expYear, cardType, currency, totalAmount, firstName, lastName, address, locality, postalCode, country, email, phone, transaction_id, capture):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    extendAuthIndicator = True
    authorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
        extend_auth_indicator = extendAuthIndicator
    )

    processingInformationActionList = []
    processingInformationActionList.append("VALIDATE_CONSUMER_AUTHENTICATION")
    processingInformationCapture = capture
    processingInformation = Ptsv2paymentsProcessingInformation(
        action_list = processingInformationActionList,
        authorization_options = authorizationOptions.__dict__,
        capture = processingInformationCapture
    )

    paymentInformationCardNumber = cardNumber
    paymentInformationCardExpirationMonth = expMonth
    paymentInformationCardExpirationYear = expYear
    paymentInformationCardType = cardType
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        number = paymentInformationCardNumber,
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear,
        type = paymentInformationCardType
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        card = paymentInformationCard.__dict__
    )

    orderInformationAmountDetailsCurrency = currency
    orderInformationAmountDetailsTotalAmount = totalAmount
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        currency = orderInformationAmountDetailsCurrency,
        total_amount = orderInformationAmountDetailsTotalAmount
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
    # if totalAmount == 0:
    #     consumerAuthenticationInformationMessageCategory = '02'

    consumerAuthenticationInformationAuthenticationTransactionId = transaction_id
    consumerAuthenticationInformation = Ptsv2paymentsConsumerAuthenticationInformation(
        message_category=consumerAuthenticationInformationMessageCategory,
        authentication_transaction_id = consumerAuthenticationInformationAuthenticationTransactionId
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
    
    print("\n----- samples/Payments/Payments/auth-with-pa-valid.py -----")
    print("\nAPI REQUEST BODY : ", requestObj)

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
    rest_auth_with_pa_valid("TC50171_3", "4000000000001091", "01", "2023", "001", "HKD",  "30.00", "John", "Smith", "201 S. Division St._1", "Foster City", "00000", "HK", "accept@cybs.com", "6504327113", "OiCtXA1j1AxtSNDh5lt1", True)
