import os
from importlib.machinery import SourceFileLoader
from typing import Any
from pathlib import Path
from zeep import Client
from zeep.wsse import BinarySignature
from zeep.plugins import Plugin
from lxml import etree
from datetime import datetime, timedelta, UTC
import uuid
from base64 import b64encode

class CyberSourceSignature(BinarySignature):
    """Custom WSSE signature implementation for CyberSource."""
    
    def apply(self, envelope, headers):
        """Apply the signature to the envelope."""
        # Add timestamp with 5 minute expiration
        now = datetime.now(UTC)
        expired = now + timedelta(minutes=5)
        timestamp_id = f'Timestamp-{uuid.uuid4()}'
        
        security = self._get_security_header(envelope)
        
        # Add Timestamp
        timestamp = etree.SubElement(
            security,
            '{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Timestamp'
        )
        timestamp.set(
            '{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Id',
            timestamp_id
        )
        
        created = etree.SubElement(
            timestamp,
            '{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Created'
        )
        created.text = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        expires = etree.SubElement(
            timestamp,
            '{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Expires'
        )
        expires.text = expired.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Apply regular binary signature
        return super().apply(envelope, headers)

def create_cybersource_client(wsdl_url: str, p12_path: str, p12_password: str) -> Client:
    """Create and configure CyberSource SOAP client with WS-Security."""
    # Create custom WSSE handler
    wsse = CyberSourceSignature(
        key_file=p12_path,
        key_password=p12_password
    )
    
    class TimestampPlugin(Plugin):
        """Plugin to add wsu:Id to Body element for signature reference."""
        def egress(self, envelope, http_headers, operation, binding_options):
            body = envelope.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
            if body is not None:
                body.set('{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd}Id', 'body')
            return envelope, http_headers

    return Client(
        wsdl=wsdl_url,
        wsse=wsse,
        plugins=[TimestampPlugin()]
    )

def process_payment(payment_data: dict) -> Any:
    """Process payment through CyberSource API."""
    try:
        # Load configuration
        config = SourceFileLoader(
            "module.name", 
            os.path.join(os.getcwd(), "utils.py")
        ).load_module()
        
        # Create client
        client = create_cybersource_client(
            config.SOAP_WSDL,
            config.SOAP_P12_FILE,
            config.SOAP_P12_PASSWORD
        )

        # Prepare transaction data
        transaction_data = {
            'merchantID': config.SOAP_USERNAME,
            'ccAuthService_run': 'true',
            'ccCaptureService_run': 'true',
            'purchaseTotals_currency': 'HKD',
            'purchaseTotals_grandTotalAmount': '1',
            **payment_data
        }

        print("\nAPI REQUEST DATA:", transaction_data)
        
        # Process transaction
        result = config.send_request(client, transaction_data)
        config.show_result(result)
        return result
        
    except KeyError:
        print('Request ID does not exist.')
    except Exception as e:
        print(f'Error processing payment: {e}')

if __name__ == '__main__':    
    test_payment = {
        'merchantReferenceCode': 'KN25032107',
        'card_accountNumber': '4000000000002503',
        'card_expirationMonth': '12',
        'card_expirationYear': '2030',
        'card_cardType': '001',
        'billTo_firstName': 'Ken',
        'billTo_lastName': 'Ngan',
        'billTo_street1': '27F Manhattan Place',
        'billTo_city': 'Kowloon Bay',
        'billTo_postalCode': '00000',
        'billTo_country': 'HK',
        'billTo_email': 'ken@example.com',
        'billTo_phoneNumber': '91360955'
    }
    process_payment(test_payment)