from pathlib import Path
import os, json, requests, random, datetime, time
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

def mpgs_retrieve_order(orderId):
    
    host = configuration.MPGS_BASE_URL
    version = configuration.MPGS_API_VERSION
    merchantId = configuration.MPGS_MERCHANT_ID
    
    url = 'https://{host}/api/rest/version/{version}/merchant/{merchantId}/order/{orderId}'.format(host=host, version=version, merchantId=merchantId, orderId=orderId)
    
    user = 'merchant.'+ merchantId
    password = configuration.MPGS_API_PASSWORD
    
    try:
        print("\nORDER ID : ", orderId)
            
        return_data = requests.get(url, auth=(user, password))
        
        print("\nAPI RESPONSE CODE : ", return_data)
        print("\nAPI RESPONSE BODY : ", return_data.content)
        
        body = return_data.content.decode('UTF-8')
        body = json.loads(body)
        
        return body
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    mpgs_retrieve_order("KN250204170246")