from CyberSource import *
from pathlib import Path
import os, json
from importlib.machinery import SourceFileLoader
import utils as utils

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

def transient_token_auth_with_pa_validation(referenceNumber, transientToken, transaction_id, flag, product):
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = referenceNumber
    )

    processingInformationActionTokenTypes = []
    processingInformationActionTokenTypes.append("customer")
    processingInformationActionTokenTypes.append("paymentInstrument")
    processingInformationActionTokenTypes.append("shippingAddress")

    processingInformationCapture = False
    if flag:
        processingInformationCapture = True
    
    processingInformationActionList = []
    processingInformationActionList.append("TOKEN_CREATE")
    processingInformationActionList.append("VALIDATE_CONSUMER_AUTHENTICATION")
    processingInformation = Ptsv2paymentsProcessingInformation(
        action_list = processingInformationActionList,
        action_token_types = processingInformationActionTokenTypes,
        capture = processingInformationCapture
    )

    tokenInformation = Ptsv2paymentsTokenInformation(
        transient_token_jwt = transientToken
    )

    if product=="microform":
        orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
            **utils.MICROFORM_BILL_TO
        )
        amountDetails = Ptsv2paymentsOrderInformationAmountDetails(
            **utils.AMOUNT_DETAILS
        )
        orderInformation = Ptsv2paymentsOrderInformation(
            amount_details=amountDetails.__dict__,
            bill_to = orderInformationBillTo.__dict__
        )
    else:
        orderInformation = Ptsv2paymentsOrderInformation()

    consumerAuthenticationInformationAuthenticationTransactionId = transaction_id
    consumerAuthenticationInformation = Ptsv2paymentsConsumerAuthenticationInformation(
        authentication_transaction_id = consumerAuthenticationInformationAuthenticationTransactionId
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        order_information=orderInformation.__dict__,
        token_information = tokenInformation.__dict__,
        consumer_authentication_information = consumerAuthenticationInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)
    
    print("\nAPI REQUEST BODY : ", requestObj)

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
    transient_token_auth_with_pa_validation("cybs_test", "eyJraWQiOiIwOFFHSzBkRWV4UzBGY2x3dmgxbEd2N3EyMEZLZnpZayIsImFsZyI6IlJTMjU2In0", "OiCtXA1j1AxtSNDh5lt1", False, "unified_checkout")
