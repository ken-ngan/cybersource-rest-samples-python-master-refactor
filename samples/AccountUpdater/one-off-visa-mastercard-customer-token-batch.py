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

def one_off_visa_mastercard_customer_token_batch():
    type = "oneOff"

    includedTokens = []
    includedTokens1 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1C998A2D8FEA2FE063AF598E0A3F10"
    )

    includedTokens.append(includedTokens1.__dict__)

    includedTokens2 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1C998A2B47EA2FE063AF598E0A3F10"
    )

    includedTokens.append(includedTokens2.__dict__)

    includedTokens3 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1C9966810AE578E063AF598E0A1CDE"
    )

    includedTokens.append(includedTokens3.__dict__)

    includedTokens4 = Accountupdaterv1batchesIncludedTokens(
        id = "3B0E5B458498F15EE063AF598E0A5CE8"
    )

    includedTokens.append(includedTokens4.__dict__)

    includedTokens5 = Accountupdaterv1batchesIncludedTokens(
        id = "3B0E622C34E5393BE063AF598E0AA5B3"
    )

    includedTokens.append(includedTokens5.__dict__)

    includedTokens6 = Accountupdaterv1batchesIncludedTokens(
        id = "3B1C8CC907A86C52E063AF598E0A7E97"
    )

    includedTokens.append(includedTokens6.__dict__)

    included = Accountupdaterv1batchesIncluded(
        tokens = includedTokens
    )

    merchantReference = "KN250730AU1"
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
    one_off_visa_mastercard_customer_token_batch()