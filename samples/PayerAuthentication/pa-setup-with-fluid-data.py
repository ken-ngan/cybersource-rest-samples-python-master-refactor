from CyberSource import *
from pathlib import Path
import os
import json
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d

def pa_setup_with_fluid_data(googlePayBlob):
    clientReferenceInformationCode = "cybs_test"
    clientReferenceInformationPartnerDeveloperId = "7891234"
    clientReferenceInformationPartnerSolutionId = "89012345"
    clientReferenceInformationPartner = Riskv1decisionsClientReferenceInformationPartner(
        developer_id = clientReferenceInformationPartnerDeveloperId,
        solution_id = clientReferenceInformationPartnerSolutionId
    )

    clientReferenceInformation = Riskv1decisionsClientReferenceInformation(
        code = clientReferenceInformationCode
        # code = clientReferenceInformationCode,
        # partner = clientReferenceInformationPartner.__dict__
    )

    paymentInformationFluidDataValue = googlePayBlob
    paymentInformationFluidData = Riskv1authenticationsetupsPaymentInformationFluidData(
        value = paymentInformationFluidDataValue
    )

    paymentInformation = Riskv1authenticationsetupsPaymentInformation(
        fluid_data = paymentInformationFluidData.__dict__
    )

    processingInformationPaymentSolution = "012"
    processingInformation = Riskv1authenticationsetupsProcessingInformation(
        payment_solution = processingInformationPaymentSolution
    )

    requestObj = PayerAuthSetupRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        processing_information = processingInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\n----- samples/PayerAuthentication/pa-setup-with-fluid-data.py -----")
    print("\nAPI REQUEST BODY : ", requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PayerAuthenticationApi(client_config)
        return_data, status, body = api_instance.payer_auth_setup(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PayerAuthenticationApi->payer_auth_setup: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    pa_setup_with_fluid_data("RklEPUVNVi5QQVlNRU5ULkFQSQ==")
