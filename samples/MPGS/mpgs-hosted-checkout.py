from pathlib import Path
import os, json, requests, datetime
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "utils.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def mpgs_hosted_checkout(operation, orderId, amount, currency):
    
    host = configuration.MPGS_BASE_URL
    version = configuration.MPGS_API_VERSION
    merchantId = configuration.MPGS_MERCHANT_ID
    
    url = 'https://{host}/api/rest/version/{version}/merchant/{merchantId}/session'.format(host=host, version=version, merchantId=merchantId)
    
    user = 'merchant.'+ merchantId
    password = configuration.MPGS_API_PASSWORD

    merchant = dict(
        name = "GP Product Test",
        url = configuration.BASE_URL
    )

    interaction = dict(
        operation = operation,
        merchant = merchant,
        returnUrl = configuration.BASE_URL + "/views/mpgs-receipt"
    )

    order = dict(
        amount = amount,
        currency = currency,
        id = orderId,
        reference = orderId,
        description = "Goods and Services"
    )
        
    requestObj = dict(
        apiOperation = "INITIATE_CHECKOUT",
        checkoutMode = "WEBSITE",
        interaction = interaction,
        order = order
    )

    requestObj = del_none(requestObj)
    requestObj = json.dumps(requestObj)
    
    try:
        print("\nPOST ", url)
        print("\nAPI REQUEST BODY : ", requestObj)
            
        return_data = requests.post(url, data=requestObj, auth=(user, password))
        
        print("\nAPI RESPONSE CODE : ", return_data)
        print("\nAPI RESPONSE BODY : ", return_data.content)
        
        body = return_data.content.decode('UTF-8')
        body = json.loads(body)
        
        # session_id = body['session']['id']
        
        return body
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling mpgs_hosted_checkout: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    # mpgs_hosted_checkout(operation, orderId, amount, currency)
    # mpgs_hosted_checkout("VERIFY", "KN2025020401", "10.00", "HKD")
    mpgs_hosted_checkout("AUTHORIZE", "KN2025020401", "10.00", "HKD")
    # mpgs_hosted_checkout("PURCHASE", "KN2025020401", "10.00", "HKD")