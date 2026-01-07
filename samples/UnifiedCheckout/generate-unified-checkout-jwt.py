from CyberSource import *
from pathlib import Path
import os
import json
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

def generate_unified_checkout_capture_context(captureMandate, amountDetails, unified_checkout_config):

    captureMandate = Upv1capturecontextsCaptureMandate(
        **captureMandate
    )

    amountDetails = Upv1capturecontextsOrderInformationAmountDetails(
        **amountDetails
    )

    orderInformation = Upv1capturecontextsOrderInformation(
        amount_details=amountDetails.__dict__
    )

    requestObj = GenerateUnifiedCheckoutCaptureContextRequest(
        **unified_checkout_config,
        capture_mandate=captureMandate.__dict__,
        order_information=orderInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)
    
    print("\nAPI REQUEST BODY : ", requestObj)
     
    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = UnifiedCheckoutCaptureContextApi(client_config)
        return_data, status, body = api_instance.generate_unified_checkout_capture_context(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        #write_log_audit(status)
        print(__name__, status, body)
        return body
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling TaxesApi->calculate_tax: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

