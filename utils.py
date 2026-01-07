"""
Utility functions for CyberSource integration.
Includes signature generation, field signing, and card scheme detection.
"""
import os
import hmac
import re
import pyfiglet
import uuid
from base64 import b64encode
from hashlib import sha256
from termcolor import colored
from pprint import pprint
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any
from zeep import Client, Transport, Plugin
from lxml import etree
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend

import config

# REQUEST BODY PARAMETERS
CAPTURE_MANDATE = dict(
    billing_type="FULL",
    request_phone=False,
    request_shipping=False,
    show_accepted_network_icons=True
)
AMOUNT_DETAILS = dict(
    total_amount="10.00",
    currency="HKD"
)
UNIFIED_CHECKOUT_CONFIG = dict(
    target_origins = [config.BASE_URL],
    client_version = "0.24",
    allowed_card_networks = ["VISA","MASTERCARD","CUP"],
    allowed_payment_types=["PANENTRY", "CLICKTOPAY", "GOOGLEPAY"], #unified checkout
    # allowed_payment_types=["CLICKTOPAY"], #click to pay
    country="HK",
    locale="en_US"
)
MICROFORM_BILL_TO = dict(
    first_name = "Joe",
    last_name = "Doe",
    address1 = "27F Manhattan Place",
    locality = "Kowloon Bay",
    country = "HK",
    email = "joe@example.com"
)
MICROFORM_CONFIG = dict(
    target_origins = [config.BASE_URL],
    client_version = "v2.0",
    allowed_card_networks = ["VISA","MASTERCARD"]
)

def create_sha256_signature(key: str, message: str) -> str:
    """
    Signs an HMAC SHA-256 signature to a message with Base 64 encoding.
    This is required by CyberSource.
    
    Args:
        key: Secret key for HMAC signing
        message: Message to sign
        
    Returns:
        Base64-encoded HMAC SHA-256 signature
        
    Raises:
        ValueError: If key or message is empty
    """
    if not key or not message:
        raise ValueError("Key and message must not be empty")
    
    digest = hmac.new(
        key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=sha256,
    ).digest()
    return b64encode(digest).decode('utf-8')

def sign_fields_to_context(
    fields: Dict[str, Any], 
    context: Dict[str, Any], 
    secret_key: str, 
    url: str
) -> Dict[str, Any]:
    """
    Builds the list of field names and data to sign, and creates the
    signature required by CyberSource Secure Acceptance.
    
    Args:
        fields: Dictionary of form fields to sign
        context: Context dictionary to update with signed fields
        secret_key: Secret key for signature generation
        url: Target URL for the form submission
        
    Returns:
        Updated context dictionary with signed fields and signature
    """
    if not secret_key:
        raise ValueError("Secret key must not be empty")
    
    # Create a copy to avoid mutating the original
    fields = fields.copy()
    
    fields['signed_date_time'] = datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace('+00:00', 'Z')
    
    signed_field_names = list(fields.keys())

    # After adding all the included fields, we need to also add
    # `unsigned_field_names` and `signed_field_names` to the data
    # to be signed.
    signed_field_names.append('unsigned_field_names')
    fields['unsigned_field_names'] = ''
    signed_field_names.append('signed_field_names')
    fields['signed_field_names'] = ','.join(signed_field_names)

    # Build the fields into a list to sign, which will become
    # a string when joined by a comma
    data_to_sign = [f'{key}={value}' for key, value in fields.items()]

    context['fields'] = fields
    context['signature'] = create_sha256_signature(
        secret_key,
        ','.join(data_to_sign),
    )
    context['url'] = url
    return context

def sop_sign_fields_to_context(
    fields: Dict[str, Any], 
    context: Dict[str, Any], 
    secret_key: str, 
    url: str
) -> Dict[str, Any]:
    """
    Builds the list of field names and data to sign for Silent Order Post (SOP),
    and creates the signature required by CyberSource.
    
    Args:
        fields: Dictionary of form fields to sign
        context: Context dictionary to update with signed fields
        secret_key: Secret key for signature generation
        url: Target URL for the form submission
        
    Returns:
        Updated context dictionary with signed fields and signature
    """
    if not secret_key:
        raise ValueError("Secret key must not be empty")
    
    # Create a copy to avoid mutating the original
    fields = fields.copy()
    
    fields['signed_date_time'] = datetime.now(timezone.utc).replace(
        microsecond=0
    ).isoformat().replace('+00:00', 'Z')
    
    signed_field_names = list(fields.keys())

    # After adding all the included fields, we need to also add
    # `unsigned_field_names` and `signed_field_names` to the data
    # to be signed.
    # SOP excludes sensitive card fields from signature
    signed_field_names.append('unsigned_field_names')
    fields['unsigned_field_names'] = 'card_number,card_expiry_date,card_type,card_cvn'
    signed_field_names.append('signed_field_names')
    fields['signed_field_names'] = ','.join(signed_field_names)

    # Build the fields into a list to sign
    data_to_sign = [f'{key}={value}' for key, value in fields.items()]

    context['fields'] = fields
    context['signature'] = create_sha256_signature(
        secret_key,
        ','.join(data_to_sign),
    )
    context['url'] = url
    return context

def mask_card(card_number: str) -> str:
    """
    Mask credit card number for display/storage.
    Shows first 6 and last 4 digits, masks the rest.
    Supports 16-19 digit cards (e.g., China UnionPay).
    
    Args:
        card_number: Credit card number to mask
        
    Returns:
        Masked card number string (e.g., "123456xxxxxx7890")
    """
    if not card_number:
        return ""
    
    # Remove any whitespace or dashes
    card_number = re.sub(r'[\s-]', '', str(card_number))
    
    # Validate minimum length
    if len(card_number) < 10:
        return "****"
    
    # Mask: first 6 digits + masked middle + last 4 digits
    return f"{card_number[:6]}{'x' * (len(card_number) - 10)}{card_number[-4:]}"


def print_emv_data_mask_the_pan(emv_track2_acsii: str) -> None:
    """
    Parse and mask EMV track 2 data, displaying card PAN and expiration.
    
    Args:
        emv_track2_acsii: EMV track 2 data in ASCII format
    """
    # Use raw string to avoid escape sequence warnings
    regex = re.compile(r"([\d]*)=([\d]{4})[\d]*")
    match = regex.match(emv_track2_acsii)
    
    if not match:
        print("Invalid EMV track 2 data format")
        return
    
    pan = match.group(1)
    exp = match.group(2)
    
    if len(pan) < 10:
        print("Invalid PAN length")
        return
    
    masked = pan[:6] + 'X' * (len(pan)-10) + pan[-4:]
    print('card: ' + masked)
    print('exp: ' + exp)

def nvp2dict(s):
    try:
        d = dict(item.strip().split('=', 1) for item in s.splitlines())
        return d
    except ValueError:
        print('response type error: \n', s)
        
def dict2nvp(d):
    try:
        s = '\r\n'.join('{!s}={!s}'.format(key, val) for (key, val) in d.items())
        return s
    except ValueError:
        print('response type error: \n', d)
        s = None

def send_request(client, data):
    r = client.service.runTransaction(dict2nvp(data))
    return nvp2dict(r)

def show_result(r):
    ascii_banner = pyfiglet.Figlet(font='banner3').renderText(r['decision'])
    if r['decision'] != 'ACCEPT':
        print(colored(ascii_banner, 'red'))
    else:
        print(colored(ascii_banner, 'green'))
    pprint(r)
    
def schemes_checker(card_number: str) -> Optional[str]:
    """
    Identify credit card scheme from card number using regex patterns.
    
    Source: https://gist.github.com/michaelkeevildown/9096cd3aac9029c4e6e05588448a8841
    
    Args:
        card_number: Credit card number (without spaces/dashes)
        
    Returns:
        Card type code string (e.g., '001' for Visa) or None if not recognized
    """
    if not card_number or not card_number.strip():
        return None
    
    # Remove any whitespace or dashes
    card_number = re.sub(r'[\s-]', '', card_number)
    
    scheme = {
        'Discover':{
            'regex': '^65[4-9][0-9]{13}|64[4-9][0-9]{13}|6011[0-9]{12}|(622(?:12[6-9]|1[3-9][0-9]|[2-8][0-9][0-9]|9[01][0-9]|92[0-5])[0-9]{10})$',
            'card_cardType': '004'
        },
        'Amex':{
            'regex': '^3[47][0-9]{13}$',
            'card_cardType': '003'
        },
        'MasterCard':{
            'regex': '^5[1-5][0-9]{14}',
            'card_cardType': '002'
        },
        'Visa':{
            'regex': '^4\\d{12}(\\d{3})?$',
            'card_cardType': '001'
        },
        'JCB':{
            'regex': '^(?:2131|1800|35\\d{3})\\d{11}',
            'card_cardType': '007'
        },
        'CUP':{
            'regex': '^(62[0-9]{14,17})$',
            'card_cardType': '062'
        }
    }
    
    for key, value in scheme.items():
        regex = r'{}'.format(value['regex'])
        match = re.match(regex, card_number)
        if match:
            return value['card_cardType']
    
    return None

##### SOAP P12 Authentication Starts #####
class SecurityPlugin(Plugin):
    """
    Zeep plugin implementing WS-Security for CyberSource SOAP API.
    Handles X.509 certificate-based authentication with SHA256 signatures.
    """

    def __init__(self, p12_path, p12_password):
        """
        Initialize security plugin with P12 certificate.
        """
        p12_data = Path(p12_path).read_bytes()
        private_key, cert, _ = pkcs12.load_key_and_certificates(
            p12_data, 
            p12_password.encode(), 
            default_backend()
        )
        self.private_key = private_key
        self.certificate = cert

    def egress(self, envelope, http_headers, operation, binding_options):
        security = self._create_security_header(envelope)
        header = envelope.find(f'.//{{{config.XML_NAMESPACES["soap"]}}}Header')
        if header is None:
            header = etree.Element(f'{{{config.XML_NAMESPACES["soap"]}}}Header')
            envelope.insert(0, header)
        header.append(security)
        return envelope, http_headers

    def _create_element(self, parent, ns, name, text=None, **attrs):
        """
        Create XML element with proper namespace.
        """
        elem = etree.SubElement(parent, f'{{{config.XML_NAMESPACES[ns]}}}{name}')
        if text:
            elem.text = text
        for key, value in attrs.items():
            elem.set(key, value)
        return elem

    def _add_reference(self, signed_info, uri, digest_value):
        """
        Add reference element to SignedInfo for WS-Security signature.
        Includes transforms, digest method and digest value.
        """
        ref = self._create_element(signed_info, 'ds', 'Reference', URI=uri)
        transforms = self._create_element(ref, 'ds', 'Transforms')
        self._create_element(transforms, 'ds', 'Transform', 
                           Algorithm=config.XML_ALGORITHMS['c14n'])
        self._create_element(ref, 'ds', 'DigestMethod',
                           Algorithm=config.XML_ALGORITHMS['digest'])
        self._create_element(ref, 'ds', 'DigestValue', text=digest_value)

    def _create_signed_info(self, body_canon, timestamp_canon, nonce):
        """
        Create SignedInfo element containing references to signed content.
        """
        signed_info = etree.Element(f'{{{config.XML_NAMESPACES["ds"]}}}SignedInfo', nsmap=config.XML_NAMESPACES)
        
        # Add methods
        self._create_element(signed_info, 'ds', 'CanonicalizationMethod',
                           Algorithm=config.XML_ALGORITHMS['c14n'])
        self._create_element(signed_info, 'ds', 'SignatureMethod',
                           Algorithm=config.XML_ALGORITHMS['sha256'])
        
        # Add references
        body_digest = b64encode(sha256(body_canon).digest()).decode()
        timestamp_digest = b64encode(sha256(timestamp_canon).digest()).decode()
        self._add_reference(signed_info, '#body', body_digest)
        self._add_reference(signed_info, f'#Timestamp-{nonce}', timestamp_digest)
        
        return signed_info

    def _create_security_header(self, envelope):
        """
        Create complete WS-Security header
        """
        # Generate nonce and timestamps
        nonce = b64encode(uuid.uuid4().bytes).decode()
        now = datetime.now(timezone.utc)
        created = now.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
        expires = (now + timedelta(minutes=5)).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

        # Create main security element
        security = etree.Element(f'{{{config.XML_NAMESPACES["wsse"]}}}Security', 
                               nsmap=config.XML_NAMESPACES)
        security.set(f'{{{config.XML_NAMESPACES["soap"]}}}mustUnderstand', '1')

        # Create timestamp
        timestamp = self._create_element(security, 'wsu', 'Timestamp', 
                                      **{f'{{{config.XML_NAMESPACES["wsu"]}}}Id': f'Timestamp-{nonce}'})
        self._create_element(timestamp, 'wsu', 'Created', text=created)
        self._create_element(timestamp, 'wsu', 'Expires', text=expires)

        # Get canonicalized forms
        body = envelope.find(f'.//{{{config.XML_NAMESPACES["soap"]}}}Body')
        body.set(f'{{{config.XML_NAMESPACES["wsu"]}}}Id', 'body')
        body_canon = etree.tostring(body, method='c14n', exclusive=True)
        timestamp_canon = etree.tostring(timestamp, method='c14n', exclusive=True)

        # Create signed info and signature
        signed_info = self._create_signed_info(body_canon, timestamp_canon, nonce)
        signed_info_canon = etree.tostring(signed_info, method='c14n', exclusive=True)
        signature_value = b64encode(self.private_key.sign(
            signed_info_canon,
            padding.PKCS1v15(),
            hashes.SHA256()
        )).decode()

        # Create security token
        cert_b64 = b64encode(self.certificate.public_bytes(serialization.Encoding.DER)).decode()
        token = self._create_element(security, 'wsse', 'BinarySecurityToken',
            text=cert_b64,
            EncodingType=config.XML_ALGORITHMS['encoding'],
            ValueType=config.XML_ALGORITHMS['x509'],
            **{f'{{{config.XML_NAMESPACES["wsu"]}}}Id': f'X509Token-{nonce}'})

        # Create signature
        signature = self._create_element(security, 'ds', 'Signature')
        signature.append(signed_info)
        self._create_element(signature, 'ds', 'SignatureValue', text=signature_value)
        
        key_info = self._create_element(signature, 'ds', 'KeyInfo')
        token_ref = self._create_element(key_info, 'wsse', 'SecurityTokenReference')
        self._create_element(token_ref, 'wsse', 'Reference',
            URI=f'#X509Token-{nonce}',
            ValueType=config.XML_ALGORITHMS['x509'])

        return security

def CyberSourceClient(wsdl_url, p12_path, p12_password):
    """
    Create CyberSource SOAP client with WS-Security authentication.
    """
    transport = Transport(timeout=30)
    security_plugin = SecurityPlugin(p12_path, p12_password)
    return Client(wsdl=wsdl_url, transport=transport, plugins=[security_plugin])
##### SOAP P12 Authentication Ends #####