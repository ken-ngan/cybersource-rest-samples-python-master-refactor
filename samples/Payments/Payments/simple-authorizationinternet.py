from CyberSource import *
from pathlib import Path
import os
import json
import time
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

def simple_authorizationinternet(referenceInfoCode, reconciliationId, cardType, cardNumber, expMonth, expYear, totalAmount, currency, firstName, lastName, address, locality, postalCode, country, email, phone, flag):
    clientReferenceInformationCode = referenceInfoCode
    clientReferenceReconciliationId = reconciliationId
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode,
        reconciliation_id=clientReferenceReconciliationId
    )

    processingInformationCapture = False
    if flag:
        processingInformationCapture = True
    
    processingInformation = Ptsv2paymentsProcessingInformation(
        capture = processingInformationCapture
    )

    paymentInformationCardType = cardType
    paymentInformationCardNumber = cardNumber
    paymentInformationCardExpirationMonth = expMonth
    paymentInformationCardExpirationYear = expYear
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        type = paymentInformationCardType,
        number = paymentInformationCardNumber,
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear,
        security_code="475"
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
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

    merchantInformationMerchantDescriptorName = " "
    merchantInformationMerchantDescriptorLocality = " "
    merchantInformationMerchantDescriptorCountry = " "
    merchantInformationMerchantDescriptor = Ptsv2paymentsMerchantInformationMerchantDescriptor(
        name = merchantInformationMerchantDescriptorName,
        locality = merchantInformationMerchantDescriptorLocality,
        country = merchantInformationMerchantDescriptorCountry
    )
    
    merchantInformation = Ptsv2paymentsMerchantInformation(
        merchant_descriptor = merchantInformationMerchantDescriptor.__dict__
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__
        # merchant_information = merchantInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        print("\nAPI RESQUEST BODY : ", requestObj)
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
    simple_authorizationinternet("KN20250818B", "KN20250818B", "002", "5289460006139437", "12", "2027", "10", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", True)
    # # time.sleep(10)
    # simple_authorizationinternet("CUP250603A", "CUP250603A", "062", "6244680109217465", "05", "2027", "1", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", False)
    # time.sleep(10)
    # simple_authorizationinternet("CUP250603B", "CUP250603B", "062", "6244680109217465", "05", "2027", "1", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", False)
    # time.sleep(10)
    # simple_authorizationinternet("CUP250603C", "CUP250603C", "062", "6244680109217465", "05", "2027", "1", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", False)
    # time.sleep(10)
    # simple_authorizationinternet("SIT_Cycle2_Task17_!\"test", "SIT_Cycle2_Task09_,-test", "062", "6244680109217465", "05", "2027", "2.25", "SGD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", True)
    # time.sleep(10)
    # simple_authorizationinternet("SIT_Cycle2_Task18_$&test", "SIT_Cycle2_Task09_,-test", "062", "6244680109217465", "05", "2027", "3.5", "SGD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", True)
    # time.sleep(10)
    # simple_authorizationinternet("KN2025011001", "KN2025011001", "002", "5289460006139437", "12", "2027", "1", "HKD", "Ken", "Ngan", "27F Manhattan Place", "Kowloon Bay", "00000", "HK", "test@cybs.com", "4158880000", False)