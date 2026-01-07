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

def refund_payment(referenceCode, totalAmount, currency, id):
    
    clientReferenceInformationCode = referenceCode
    clientReferenceInformationReconciliationId = referenceCode
    clientReferenceInformation = Ptsv2paymentsidrefundsClientReferenceInformation(
        code = clientReferenceInformationCode,
        reconciliation_id=clientReferenceInformationReconciliationId
    )

    orderInformationAmountDetailsTotalAmount = totalAmount
    orderInformationAmountDetailsCurrency = currency
    orderInformationAmountDetails = Ptsv2paymentsidcapturesOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformation = Ptsv2paymentsidrefundsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__
    )

    requestObj = RefundPaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        order_information = orderInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = RefundApi(client_config)
        return_data, status, body = api_instance.refund_payment(requestObj, id)

        print("\nAPI REQUEST BODY : ", requestObj)
        print("\nTRANSACTION ID : ", id)
        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling RefundApi->refund_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    refund_payment("test_cybs", "6.00", "HKD", "7568713334326032003852")