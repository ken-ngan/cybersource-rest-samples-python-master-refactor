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

def capture_payment(id):
    clientReferenceInformationCode = "TC50171_3"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    orderInformationAmountDetailsTotalAmount = "10"
    orderInformationAmountDetailsCurrency = "HKD"
    orderInformationAmountDetails = Ptsv2paymentsidcapturesOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformation = Ptsv2paymentsidcapturesOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__
    )

    requestObj = CapturePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        order_information = orderInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        capture_api_instance = CaptureApi(client_config)
        return_data, status, body = capture_api_instance.capture_payment(requestObj, id)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        rid = return_data.id
        
        print("\nRID : ", rid)
    
        transaction_config_obj = configuration.Configuration()
        transaction_client_config = transaction_config_obj.get_configuration()
        # time.sleep(15)
        transaction_api_instance = TransactionDetailsApi(transaction_client_config)
        transaction_return_data, transaction_status, transaction_body = transaction_api_instance.get_transaction(rid)

        print("\nAPI RESPONSE CODE : ", transaction_status)
        print("\nAPI RESPONSE BODY : ", transaction_body)

        return transaction_return_data
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    capture_payment("7237774253646003203955")