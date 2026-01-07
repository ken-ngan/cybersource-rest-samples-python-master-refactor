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

def mpgs_transaction(apiOperation, orderId, targetTransactionId, amount, currency, number, month, year, securityCode):
    
    host = configuration.MPGS_BASE_URL
    version = configuration.MPGS_API_VERSION
    merchantId = configuration.MPGS_MERCHANT_ID
    transaction_id = random.randint(1,999999999)
    
    if apiOperation == 'VERIFY' or apiOperation == 'AUTHORIZE' or apiOperation == 'PAY':
        orderId = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
    
    url = 'https://{host}/api/rest/version/{version}/merchant/{merchantId}/order/{orderId}/transaction/{transaction_id}'.format(host=host, version=version, merchantId=merchantId, orderId=orderId, transaction_id=transaction_id)
    
    user = 'merchant.'+ merchantId
    password = configuration.MPGS_API_PASSWORD
    
    if apiOperation == 'VERIFY' or apiOperation == 'AUTHORIZE' or apiOperation == 'PAY':
        type = "CARD"
        order = dict(
            amount = amount,
            currency = currency,
            reference = orderId
        )
        transaction = dict()
    elif apiOperation == 'CAPTURE' or apiOperation == 'VOID' or apiOperation == 'REFUND':
        type = None
        order = dict()
        transaction = dict(
            amount = amount,
            currency = currency,
            targetTransactionId = targetTransactionId
        )
    else:
        print('*** INVALID_REQUEST: Unknown apiOperation. ***')

    expiry = dict(
        month = month,
        year = year
    )
    
    card = dict(
        number = number,
        expiry = expiry,
        securityCode = securityCode
    )
    
    provided = dict(
        card = card
    )
    
    sourceOfFunds = dict(
        type = type,
        provided = provided
    )
    
    requestObj = dict(
        apiOperation = apiOperation,
        order = order,
        transaction = transaction,
        sourceOfFunds = sourceOfFunds
    )

    requestObj = del_none(requestObj)
    requestObj = json.dumps(requestObj)
    
    try:
    
        print("\nAPI REQUEST BODY : ", requestObj)
            
        return_data = requests.put(url, data=requestObj, auth=(user, password))
        
        print("\nAPI RESPONSE CODE : ", return_data)
        print("\nAPI RESPONSE BODY : ", return_data.content)
        
        return return_data
    
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    # mpgs_transaction(apiOperation, orderId, targetTransactionId, amount, currency, number, month, year, securityCode)
    # mpgs_transaction("VERIFY", None, None, None, "HKD", "5289460006139437", "12", "27", "475")
    # mpgs_transaction("AUTHORIZE", None, None, "10.00", "HKD", "5289460006139437", "12", "27", "475")
    # mpgs_transaction("PAY", None , None, "10.00", "HKD", "5289460006139437", "12", "27", "475")
    # mpgs_transaction("VOID", "KN250110160949", "458832526" , None, None, None, None, None, None)
    # mpgs_transaction("REFUND", "KN250110161848", "811778679" , "10.00", "HKD", None, None, None, None)
    mpgs_transaction("VOID", "KN250204174219", "1" , None, None, None, None, None, None)
    time.sleep(5)
    mpgs_transaction("VOID", "KN250204180020", "1" , None, None, None, None, None, None)