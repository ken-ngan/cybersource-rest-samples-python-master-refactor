from CyberSource import *
from pathlib import Path
import os, json
from importlib.machinery import SourceFileLoader
import utils as utils
import config as config

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

def transient_token_auth_with_pa_enroll(referenceNumber, transientToken, referenceId, flag, product):
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
    processingInformationActionList.append("CONSUMER_AUTHENTICATION")
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
        consumerAuthenticationInformationReturnURL = config.BASE_URL+"/views/microform-validation"
    else:
        orderInformation = Ptsv2paymentsOrderInformation()
        consumerAuthenticationInformationReturnURL = config.BASE_URL+"/views/unified-checkout-validation"
        
    consumerAuthenticationInformation = Ptsv2paymentsConsumerAuthenticationInformation(
        return_url = consumerAuthenticationInformationReturnURL,
        reference_id = referenceId
    )


    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        order_information=orderInformation.__dict__,
        consumer_authentication_information = consumerAuthenticationInformation.__dict__,
        token_information = tokenInformation.__dict__
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
    transient_token_auth_with_pa_enroll("eyJraWQiOiIwOFFHSzBkRWV4UzBGY2x3dmgxbEd2N3EyMEZLZnpZayIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJGbGV4LzA3IiwiZXhwIjoxNzE2ODg5MjI4LCJ0eXBlIjoiZ2RhLTAuOS4wIiwiaWF0IjoxNzE2ODg4MzI4LCJqdGkiOiIxRTJQRVhGSERZUjVIRFlDTENOV1A5VkgwWkVSSERWQUJFMkpaSTBBRFg5U09GMTRRSkU1NjY1NUE2OENBMjM5IiwiY29udGVudCI6eyJvcmRlckluZm9ybWF0aW9uIjp7ImJpbGxUbyI6eyJsYXN0TmFtZSI6e30sImZpcnN0TmFtZSI6e30sImNvdW50cnkiOnt9LCJhZGRyZXNzMSI6e30sInBvc3RhbENvZGUiOnt9LCJsb2NhbGl0eSI6e30sImJ1aWxkaW5nTnVtYmVyIjp7fX0sImFtb3VudERldGFpbHMiOnsidG90YWxBbW91bnQiOnt9LCJjdXJyZW5jeSI6e319fSwicGF5bWVudEluZm9ybWF0aW9uIjp7ImNhcmQiOnsiZXhwaXJhdGlvblllYXIiOnsidmFsdWUiOiIyMDI3In0sIm51bWJlciI6eyJtYXNrZWRWYWx1ZSI6IlhYWFhYWFhYWFhYWDExMTEiLCJiaW4iOiI0MTExMTEifSwic2VjdXJpdHlDb2RlIjp7fSwiZXhwaXJhdGlvbk1vbnRoIjp7InZhbHVlIjoiMTIifSwidHlwZSI6eyJ2YWx1ZSI6IjAwMSJ9fX19fQ.Lvp-HUg26dgvtu6CwnDFehDCgRPb7iGeiAtUNnu4XrUFhARCzuJcL-3JolDR7Y21Az3r2qW8qOXNljy7Abl7nK1X-FGcV4PIwHc6bLwbcD5jKLSdKWao97A2kFkhV_8s_YKtAos7DfLw3QraSccJfv9we1zpQ4to9UhY-oKrLHnQ3eAP5wyShCtIT0DP3lCTMkiaVJOKgZDlU1Uy9IWV0zgKhsvZIgQkD8DzQfY6da-t5djGkN_yasgYovDveRzJ-xSt7GEcRNGUwImvxPnF4J4sQ8QEj3d-512oV_nl55cU24dyaALaFbwhLmdBDv5L7wXbR915p433YM0PuPbeBg", "1591f14f-f862-4c6f-9bce-61057df03ed9", False)
