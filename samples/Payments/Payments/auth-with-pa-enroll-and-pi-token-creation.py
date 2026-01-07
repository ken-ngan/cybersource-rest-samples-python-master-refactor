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

def auth_with_pa_enroll_and_pi_token_creation(referenceInfoCode, cardNumber, expMonth, expYear, cvv, cardType, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phone, returnUrl, referenceId, capture):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    processingInformationRecurringOptionsFirstRecurringPayment = True
    
    processingInformationRecurringOptions = Ptsv2paymentsProcessingInformationRecurringOptions(
        first_recurring_payment = processingInformationRecurringOptionsFirstRecurringPayment
    )
    
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason = "7"
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction(
        reason = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason
    )
    
    processingInformationAuthorizationOptionsInitiatorCredentialStoredOnFile = True

    
    processingInformationAuthorizationOptionsInitiator = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiator(
        merchant_initiated_transaction = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction.__dict__,
        credential_stored_on_file = processingInformationAuthorizationOptionsInitiatorCredentialStoredOnFile
    )

    processingInformationAuthorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
        initiator = processingInformationAuthorizationOptionsInitiator.__dict__
    )

    processingInformationActionList = []
    processingInformationActionList.append("CONSUMER_AUTHENTICATION")
    processingInformationActionList.append("TOKEN_CREATE")

    processingInformationActionTokenTypes = []
    processingInformationActionTokenTypes.append("customer")
    processingInformationActionTokenTypes.append("paymentInstrument")
    processingInformationCapture = capture
    processingInformationCommerceIndicator = "internet"
    processingInformation = Ptsv2paymentsProcessingInformation(
        commerce_indicator = processingInformationCommerceIndicator,
        recurring_options = processingInformationRecurringOptions.__dict__,
        authorization_options = processingInformationAuthorizationOptions.__dict__,
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
    #     customer = paymentInformationCustomer.__dict__,
        card = paymentInformationCard.__dict__
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

    # tokenInformationPaymentInstrument_default = True
    # tokenInformationPaymentInstrument = Ptsv2paymentsTokenInformationPaymentInstrument(
    #     default = tokenInformationPaymentInstrument_default
    # )

    # tokenInformation = Ptsv2paymentsTokenInformation(
    #     payment_instrument = tokenInformationPaymentInstrument.__dict__
    # )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__,
        # token_information = tokenInformation.__dict__,
        consumer_authentication_information = consumerAuthenticationInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\n----- samples/Payments/Payments/auth-with-pa-enroll-and-pi-token-creation.py -----")
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
    auth_with_pa_enroll_and_pi_token_creation("TC5012345", "4111111111111111", "12", "2031", "123", "001", "123.45", "USD", "John", "Doe", "1 Market St", "san francisco", "00000", "HK", "test@cybs.com", "4158880000", "http://127.0.0.1:8000/views/token", "1591f14f-f862-4c6f-9bce-61057df03ed9", False)
