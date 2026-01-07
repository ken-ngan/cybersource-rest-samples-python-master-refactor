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

def auth_with_customer_token(referenceInfoCode, customerId, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phone):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason = "7"
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionID = "385289373590110"
    paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction(
        reason = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason,
        previous_transaction_id = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionID
    )

    processingInformationAuthorizationOptionsInitiatorType = "merchant"
    processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed = True
    
    processingInformationAuthorizationOptionsInitiator = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiator(
        merchant_initiated_transaction = paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction.__dict__,
        type = processingInformationAuthorizationOptionsInitiatorType,
        stored_credential_used=processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed
    )

    processingInformationAuthorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
        initiator = processingInformationAuthorizationOptionsInitiator.__dict__
    )

    processingInformationCapture = True
    processingInformationCommerceIndicator = "recurring"
    processingInformation = Ptsv2paymentsProcessingInformation(
        authorization_options = processingInformationAuthorizationOptions.__dict__,
        commerce_indicator = processingInformationCommerceIndicator,
        capture = processingInformationCapture
    )

    paymentInformationCustomerId = customerId
    paymentInformationCustomer = Ptsv2paymentsPaymentInformationCustomer(
        id = paymentInformationCustomerId
    )

    cardExpirationMonth = "0"
    cardExpirationYear = "0"
    # cardType = "001"
    card = Tmsv2customersEmbeddedDefaultPaymentInstrumentCard(
        expiration_month = cardExpirationMonth,
        expiration_year = cardExpirationYear
        # type = cardType
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        # card = card.__dict__,
        customer = paymentInformationCustomer.__dict__
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

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__
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
    auth_with_customer_token("MIT_MPAN_25101601", "4144FC977FB69E75E0631D588D0A90A6", "10.00", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "ken.ngan@globalpay.com", "4158880000")