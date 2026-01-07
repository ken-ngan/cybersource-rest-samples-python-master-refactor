import json, os
from importlib.machinery import SourceFileLoader
from pathlib import Path
from jose import jwe
from CyberSource import *
from create_instrument_identifier_card_enroll_for_network_token import create_instrument_identifier_card_enroll_for_network_token


config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()


def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


def payment_credentials_from_network_token(token_id=None):
    profile_id = "6F452100-8B79-47D5-94D6-C1AD711208D6"
    if token_id is None:
        # token_id = create_instrument_identifier_card_enroll_for_network_token().id
        token_id = "7483971883016610403867"

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = TokenApi(client_config)
        post_payment_credentials_request = PostPaymentCredentialsRequest()
        post_payment_credentials_request = del_none(post_payment_credentials_request.__dict__)
        post_payment_credentials_request = json.dumps(post_payment_credentials_request)
        print("\nAPI REQUEST BODY : ", post_payment_credentials_request)
        return_data, status, body = api_instance.post_token_payment_credentials(token_id, post_payment_credentials_request)
        # return_data, status, body = api_instance.post_token_payment_credentials(token_id, post_payment_credentials_request, profile_id=profile_id)
        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)
        
        private_key_pem_path = os.path.join(os.getcwd(), "resources", "MLE", "PROD", "gphkrecurring", "private_key.pem")

        with open(private_key_pem_path, "rb") as f:
            private_key_pem = f.read()

        # Example JWE token
        jwe_token = return_data

        try:
            decrypted_payload = jwe.decrypt(jwe_token, private_key_pem).decode('utf-8')
            print("Decrypted payload:", decrypted_payload)
            json_object = json.loads(decrypted_payload)
            print("cryptogram: ", json_object['tokenizedCard']['cryptogram'])
        except Exception as e:
            print("Error:", str(e))


        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling TokenAPI->payment-credentials API: %s\n" % e)


def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")


if __name__ == "__main__":
    payment_credentials_from_network_token()