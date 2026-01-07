import os
from importlib.machinery import SourceFileLoader

def load_sample_module(path_parts):
    """Helper to load a module from a list of path parts."""
    path = os.path.join(os.getcwd(), "samples", *path_parts)
    return SourceFileLoader("module.name", path).load_module()

### REST API ###
# REST API : Payer Authentication Setup
rest_pa_setup_with_card_number = load_sample_module(["PayerAuthentication", "pa-setup-with-card-number.py"])
rest_pa_setup_with_pi_token = load_sample_module(["PayerAuthentication", "pa-setup-with-pi-token.py"])

# REST API : Payer Authentication Enroll
rest_auth_with_pa_enroll = load_sample_module(["Payments", "Payments", "auth-with-pa-enroll.py"])
rest_auth_with_pa_enroll_and_pi_token_creation = load_sample_module(["Payments", "Payments", "auth-with-pa-enroll-and-pi-token-creation.py"])
rest_auth_with_pa_enroll_and_pi_token = load_sample_module(["Payments", "Payments", "auth-with-pa-enroll-and-pi-token.py"])

# REST API : Payer Authentication Validation
rest_auth_with_pa_valid = load_sample_module(["Payments", "Payments", "auth-with-pa-valid.py"])
rest_auth_with_pa_valid_and_pi_token_creation = load_sample_module(["Payments", "Payments", "auth-with-pa-valid-and-pi-token-creation.py"])
rest_auth_with_pa_valid_and_pi_token = load_sample_module(["Payments", "Payments", "auth-with-pa-valid-and-pi-token.py"])

# REST API : Google Pay
rest_google_pay_pa_setup = load_sample_module(["PayerAuthentication", "pa-setup-with-fluid-data.py"])
rest_google_pay_auth_pa_enroll = load_sample_module(["Payments", "Payments", "google-pay-auth-pa-enroll.py"])
rest_google_pay_auth_pa_valid = load_sample_module(["Payments", "Payments", "google-pay-auth-pa-valid.py"])
rest_google_pay_auth = load_sample_module(["Payments", "Payments", "google-pay-auth.py"])

# REST API : Token Management
retrieve_payment_instrument = load_sample_module(["TokenManagement", "PaymentInstrument", "retrieve-payment-instrument.py"])
retrieve_instrument_identifier = load_sample_module(["TokenManagement", "InstrumentIdentifier", "retrieve-instrument-identifier.py"])
delete_payment_instrument = load_sample_module(["TokenManagement", "PaymentInstrument", "delete-payment-instrument.py"])
retrieve_customer = load_sample_module(["TokenManagement", "Customer", "retrieve-customer.py"])
delete_customer = load_sample_module(["TokenManagement", "Customer", "delete-customer.py"])

# REST API : Other operations
void_payment = load_sample_module(["Payments", "Void", "void-payment.py"])
refund_payment = load_sample_module(["Payments", "Refund", "refund-payment.py"])

# REST API : Transaction Search and Reporting
retrieve_transaction = load_sample_module(["TransactionDetails", "retrieve-transaction.py"])
search_transaction = load_sample_module(["TransactionSearch", "create-search-request.py"])
query_report = load_sample_module(["Reporting", "Reports", "retrieve-available-reports.py"])
retrieve_report = load_sample_module(["Reporting", "Reports", "get-report-based-on-report-id.py"])
download_report = load_sample_module(["Reporting", "ReportDownloads", "download-report.py"])

# REST API : Generate Unified Checkout JWT
generate_unified_checkout_jwt = load_sample_module(["UnifiedCheckout", "generate-unified-checkout-jwt.py"])

# REST API : Generate Microform JWT
generate_microform_jwt = load_sample_module(["UnifiedCheckout", "generate-microform-jwt.py"])

# REST API : PA Setup using transient token
transient_token_pa_setup = load_sample_module(["UnifiedCheckout", "transient-token-pa-setup.py"])

# REST API : Authorization with PA Enroll using transient token
transient_token_auth_with_pa_enroll = load_sample_module(["UnifiedCheckout", "transient-token-auth-with-pa-enroll.py"])

# REST API : Authorization with PA Validation using transient token
transient_token_auth_with_pa_validation = load_sample_module(["UnifiedCheckout", "transient-token-auth-with-pa-validation.py"])

### SOAP ###
# SOAP : Payer Authentication Setup
soap_pa_setup_with_card_number = load_sample_module(["SimpleOrderAPI", "pa-setup-with-card-number.py"])
soap_pa_setup_with_cus_token = load_sample_module(["SimpleOrderAPI", "pa-setup-with-cus-token.py"])

# SOAP : Payer Authentication Enroll
soap_auth_with_pa_enroll = load_sample_module(["SimpleOrderAPI", "auth-with-pa-enroll.py"])
soap_auth_with_pa_enroll_and_cus_token_creation = load_sample_module(["SimpleOrderAPI", "auth-with-pa-enroll-and-cus-token-creation.py"])
soap_auth_with_pa_enroll_and_cus_token = load_sample_module(["SimpleOrderAPI", "auth-with-pa-enroll-and-cus-token.py"])

# SOAP : Payer Authentication Validation
soap_auth_with_pa_valid = load_sample_module(["SimpleOrderAPI", "auth-with-pa-valid.py"])
soap_auth_with_pa_valid_and_cus_token_creation = load_sample_module(["SimpleOrderAPI", "auth-with-pa-valid-and-cus-token-creation.py"])
soap_auth_with_pa_valid_and_cus_token = load_sample_module(["SimpleOrderAPI", "auth-with-pa-valid-and-cus-token.py"])

# SOAP : Google Pay
soap_google_pay_auth = load_sample_module(["SimpleOrderAPI", "google-pay-auth.py"])

# SOAP : Token Management
soap_retrieve_token = load_sample_module(["SimpleOrderAPI", "retrieve-token.py"])

# SOAP : Other operations
soap_afs = load_sample_module(["SimpleOrderAPI", "afs.py"])

# MPGS : Hosted Checkout
mpgs_hosted_checkout = load_sample_module(["MPGS", "mpgs-hosted-checkout.py"])
mpgs_retrieve_order = load_sample_module(["MPGS", "mpgs-retrieve-order.py"])

# MySQL
connect_mydb_path = os.path.join(os.getcwd(), "mydatabase.py")
connect_mydb = SourceFileLoader("module.name", connect_mydb_path).load_module()