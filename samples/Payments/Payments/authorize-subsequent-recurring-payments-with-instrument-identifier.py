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

def authorize_subsequent_recurring_payments_with_instrument_identifier(clientReferenceCode, previousTransactionId, instrumentIdentifierId, totalAmount, currency):
    clientReferenceInformationCode = clientReferenceCode
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )
    
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason = "07"
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionId = previousTransactionId
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction(
        reason = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionReason,
        previous_transaction_id = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionId
    )
    
    processingInformationAuthorizationOptionsInitiatorType = "merchant"
    processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed = True
    processingInformationAuthorizationOptionsInitiator = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiator(
        type = processingInformationAuthorizationOptionsInitiatorType,
        stored_credential_used = processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed,
        merchant_initiated_transaction = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction.__dict__
    )
    
    processingInformationAuthorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
        initiator = processingInformationAuthorizationOptionsInitiator.__dict__
    )
    
    processingInformationCommerceIndicator = "recurring_internet"
    processingInformation = Ptsv2paymentsProcessingInformation(
        commerce_indicator = processingInformationCommerceIndicator,
        authorization_options = processingInformationAuthorizationOptions.__dict__
    )

    paymentInformationInstrumentIdentifierId = instrumentIdentifierId
    paymentInformationInstrumentIdentifier = Ptsv2paymentsPaymentInformationInstrumentIdentifier(
        id = paymentInformationInstrumentIdentifierId
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        instrument_identifier = paymentInformationInstrumentIdentifier.__dict__
    )

    orderInformationAmountDetailsTotalAmount = totalAmount
    orderInformationAmountDetailsCurrency = currency
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__,
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


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
    authorize_subsequent_recurring_payments_with_instrument_identifier("TC50171_3", "0712MCC034785", "FF285CF3AFFBBDC0E053A2598D0AD71E", "102.21", "HKD")
