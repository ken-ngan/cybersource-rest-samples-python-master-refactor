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

def google_pay_auth_pa_valid(flag, referenceCode, googlePayBlob, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phoneNumber, transaction_id):
    clientReferenceInformationCode = referenceCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    processingInformationCapture = False
    if flag:
        processingInformationCapture = True

    processingInformationActionList = []
    processingInformationActionList.append("VALIDATE_CONSUMER_AUTHENTICATION")

    processingInformationPaymentSolution = "012"
    processingInformation = Ptsv2paymentsProcessingInformation(
        capture = processingInformationCapture,
        action_list = processingInformationActionList,
        payment_solution = processingInformationPaymentSolution
    )

    paymentInformationFluidDataValue = googlePayBlob
    paymentInformationFluidData = Ptsv2paymentsPaymentInformationFluidData(
        value = paymentInformationFluidDataValue
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        fluid_data = paymentInformationFluidData.__dict__
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
    orderInformationBillToPhoneNumber = phoneNumber
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

    consumerAuthenticationInformationAuthenticationTransactionId = transaction_id
    consumerAuthenticationInformation = Ptsv2paymentsConsumerAuthenticationInformation(
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
    
    print("\n----- samples/Payments/Payments/google-pay-auth-pa-valid.py -----")
    print("\nAPI REQUEST BODY : ", requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        return_data, status, body = api_instance.create_payment(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return body
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    google_pay_auth_pa_valid(False, "test_google_pay", "RklEPUVNVi5QQVlNRU5ULkFQSQ==", "100", "HKD", "Ken", "Ngan", "27/F, Manhattan Place", "Kowloon Bay", "00000", "HK", "ken.ngan@globalpay.com", "35293565", "OiCtXA1j1AxtSNDh5lt1")
