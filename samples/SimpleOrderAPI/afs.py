import os, pandas, time
from datetime import datetime, timedelta, UTC
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "utils.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

def afs(cardNumber):
    config_file = os.path.join(os.getcwd(), "utils.py")
    configuration = SourceFileLoader("module.name", config_file).load_module()
    
    wsdl = configuration.AFS_SOAP_WSDL
    p12_file = configuration.AFS_SOAP_P12_FILE
    p12_password = configuration.AFS_SOAP_P12_PASSWORD
    merchant_id = configuration.AFS_SOAP_USERNAME
    
    client = configuration.CyberSourceClient(wsdl, p12_file, p12_password)

    data_transaction = {}
    
    data_transaction['billTo_city'] = 'Mountain View'
    data_transaction['billTo_country'] = 'HK'
    data_transaction['billTo_email'] = 'null@cybersource.com'
    data_transaction['billTo_firstName'] = 'John'
    data_transaction['billTo_lastName'] = 'Doe'
    data_transaction['billTo_postalCode'] = '00000'
    data_transaction['billTo_street1'] = '1295 Charleston Road'
    
    data_transaction['card_accountNumber'] = cardNumber
    data_transaction['afsService_run'] = 'true'
    
    data_transaction['merchantID'] = merchant_id
    data_transaction['merchantReferenceCode'] = "KN"+datetime.now(UTC).strftime("%-y%m%d%H%M%S")
    
    data_transaction['purchaseTotals_currency'] = 'HKD'
    data_transaction['purchaseTotals_grandTotalAmount'] = "1.00"
    
    # print("\nAPI REQUEST BODY : ", data_transaction)
    
    try:
        result = configuration.send_request(client, data_transaction)
        # configuration.show_result(result)
        return result
    except (KeyError):
        print('Request ID is not exist.')

def luhn_checksum(number):
    """Calculate Luhn algorithm checksum for a number."""
    digits = [int(d) for d in str(number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(even_digits)
    for d in odd_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10

def generate_credit_card_number(bin_prefix):
    """Generate a credit card number with given BIN and valid Luhn checksum."""
    # Validate BIN
    if not (6 <= len(str(bin_prefix)) <= 8):
        raise ValueError("BIN must be 6 to 8 digits long")
    if not str(bin_prefix).isdigit():
        raise ValueError("BIN must contain only digits")
    
    # Standard credit card length is 16 digits
    total_length = 16
    bin_str = str(bin_prefix)
    remaining_length = total_length - len(bin_str) - 1  # -1 for check digit
    
    if remaining_length < 0:
        raise ValueError("BIN is too long for a 16-digit card number")
    
    # Fill remaining digits with zeros
    card_number = bin_str + '0' * remaining_length
    
    # Calculate Luhn check digit
    checksum = luhn_checksum(card_number)
    check_digit = (10 - checksum) % 10
    
    # Append check digit
    final_number = card_number + str(check_digit)
    
    return final_number

if __name__ == "__main__":
    
    # afs("4000000000002503")
    
    """Batch validate BIN."""
    df = pandas.DataFrame()
    
    try:
        test_bins = [432565, 541180, 552343, 544729, 376399, 450936, 528946, 496657, 518542, 457492, 436605, 493897, 433668, 486330, 483519, 496604, 405803, 420184, 543122, 485977]
        
        for bin_prefix in test_bins:
            card_number = generate_credit_card_number(bin_prefix)
            print(f"BIN: {bin_prefix}, Generated Card Number: {card_number}")
            result = afs(card_number)
            df = df._append(result, ignore_index=True)
            time.sleep(1)
            
        df.to_csv("afs_result_"+datetime.now(UTC).strftime("%-y%m%d%H%M%S")+".csv", index=False)
        
    except ValueError as e:
        print(f"Error: {e}")
