from CyberSource import *
import os
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
        elif isinstance(value, list):
            for item in value:
                del_none(item)
    return d

def amex_registration_customer_token_batch():
    type = "amexRegistration"

    includedTokens = []
    includedTokens1 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1CCB67F7BBA7A9E063AF598E0A8A43"
    )

    includedTokens.append(includedTokens1.__dict__)

    includedTokens2 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1CCFEC20458C28E063AF598E0A5E81"
    )

    includedTokens.append(includedTokens2.__dict__)

    includedTokens3 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1CA1D529830CDEE063AF598E0ACDC0"
    )

    includedTokens.append(includedTokens3.__dict__)

    included = Accountupdaterv1batchesIncluded(
        tokens = includedTokens
    )

    merchantReference = "KN250730AU2"
    notificationEmail = "ken.ngan@globalpay.com"
    requestObj = Body(
        type = type,
        included = included.__dict__,
        merchant_reference = merchantReference,
        notification_email = notificationEmail
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\nAPI RESQUEST BODY : ", requestObj)
    
    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = BatchesApi(client_config)
        return_data, status, body = api_instance.post_batch(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)

        return return_data
    except Exception as e:
        write_log_audit(e.status)
        print("\nException when calling BatchesApi->post_batch: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    amex_registration_customer_token_batch()