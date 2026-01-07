from CyberSource import *
from pathlib import Path
import os
import json
import base64
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

def digital_payments_applepay(paymentData):
    clientReferenceInformationCode = "TC_1231223"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    # processingInformationAuthorizationOptionsInitiatorCredentialStoredOnFile = True
    
    # processingInformationAuthorizationOptionsInitiator = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiator(
    #     credential_stored_on_file = processingInformationAuthorizationOptionsInitiatorCredentialStoredOnFile
    # )

    # processingInformationAuthorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
    #     initiator = processingInformationAuthorizationOptionsInitiator.__dict__
    # )

    processingInformationCapture = True

    processingInformationPaymentSolution = "001"
    processingInformation = Ptsv2paymentsProcessingInformation(
        # authorization_options = processingInformationAuthorizationOptions.__dict__,
        capture = processingInformationCapture,
        payment_solution = processingInformationPaymentSolution
    )


    paymentInformationFluidDataValue = paymentData
    paymentInformationFluidDataDescriptor = "RklEPUNPTU1PTi5BUFBMRS5JTkFQUC5QQVlNRU5U"
    paymentInformationFluidDataEncoding = "Base64"
    paymentInformationFluidData = Ptsv2paymentsPaymentInformationFluidData(
        value = paymentInformationFluidDataValue,
        descriptor = paymentInformationFluidDataDescriptor,
        encoding = paymentInformationFluidDataEncoding
    )

    # paymentInformationTokenizedCardNumber = "4111111111111111"
    # paymentInformationTokenizedCardExpirationMonth = "12"
    # paymentInformationTokenizedCardExpirationYear = "2031"
    paymentInformationTokenizedCardCryptogram = "AceY+igABPs3jdwNaDg3MAACAAA="
    paymentInformationTokenizedCardTransactionType = "1"
    paymentInformationTokenizedCard = Ptsv2paymentsPaymentInformationTokenizedCard(
        # number = paymentInformationTokenizedCardNumber,
        # expiration_month = paymentInformationTokenizedCardExpirationMonth,
        # expiration_year = paymentInformationTokenizedCardExpirationYear,
        cryptogram = paymentInformationTokenizedCardCryptogram,
        transaction_type = paymentInformationTokenizedCardTransactionType
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        fluid_data = paymentInformationFluidData.__dict__,
        tokenized_card = paymentInformationTokenizedCard.__dict__
    )

    orderInformationAmountDetailsTotalAmount = "10"
    orderInformationAmountDetailsCurrency = "HKD"
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformationBillToFirstName = "John"
    orderInformationBillToLastName = "Deo"
    orderInformationBillToAddress1 = "901 Metro Center Blvd"
    orderInformationBillToLocality = "Foster City"
    orderInformationBillToAdministrativeArea = "CA"
    orderInformationBillToPostalCode = "94404"
    orderInformationBillToCountry = "US"
    orderInformationBillToEmail = "test@cybs.com"
    orderInformationBillToPhoneNumber = "6504327113"
    orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
        first_name = orderInformationBillToFirstName,
        last_name = orderInformationBillToLastName,
        address1 = orderInformationBillToAddress1,
        locality = orderInformationBillToLocality,
        administrative_area = orderInformationBillToAdministrativeArea,
        postal_code = orderInformationBillToPostalCode,
        country = orderInformationBillToCountry,
        email = orderInformationBillToEmail,
        phone_number = orderInformationBillToPhoneNumber
    )

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__,
        bill_to = orderInformationBillTo.__dict__
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    print("\n----- samples/Payments/Payments/digital-payments-applepay.py -----")
    print("\nAPI REQUEST BODY : ", requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        return_data, status, body = api_instance.create_payment(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)
        return return_data
    except Exception as e:
        write_log_audit(e.status if hasattr(e, 'status') else 999)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    digital_payments_applepay("eyJkYXRhIjoiY0Ywd3lTRElvT3Y4d2JhM1BnalZkN0tsQVNVdzRwVVJpRXRjdVd6bUhJeEl1cFltbTVUT1dPczhFVjhBeGVyZG13bFJ0bHg3TG9oSmhENUpQRmJiQmdjV3RDTUpLcEwzVXZGOHVibDVtbjhTM0dLWCtOU0pjTGVyYzM2Y3hKLzd5NktxeHU5Y2FmT0t1K094OUkvUy9LYUN6eXVza3F0T0V6dGJJajZGMGQxTVRWQUd3Q1VTckpUNXQ3dGkvMnVtclIrVjM1UjBiWWVOZ2tmc2d2QUlpY2JXUG03S2w2bi9oY1pHaDhZaDdLOW5GWHJHTk1vKzlDMWZoRWZaa21ac05xckhISnJ4WDF3VG9WTnB4MGM0Ny9vL0xtVjdCTjRLK1RObkc1UStrRjVKYUZiUnk4WjRrTVRyNUJINUJVZjdJTE9kTmhTdGIxSnVNa2Z4S1hnM1VVN1BkZnFrUjl3Ukx5TVN6K05yZWlYWWttWVEwRnkydCtyQXJBWDZXVHFPUXFlZXdGUFlCTEJ4b1loT2QxQU1ybytOM0NEQlVZUkVYV09nMGczRU5Sbz0iLCJzaWduYXR1cmUiOiJNSUFHQ1NxR1NJYjNEUUVIQXFDQU1JQUNBUUV4RFRBTEJnbGdoa2dCWlFNRUFnRXdnQVlKS29aSWh2Y05BUWNCQUFDZ2dEQ0NBK013Z2dPSW9BTUNBUUlDQ0JaalRJc09NRmNYTUFvR0NDcUdTTTQ5QkFNQ01Ib3hMakFzQmdOVkJBTU1KVUZ3Y0d4bElFRndjR3hwWTJGMGFXOXVJRWx1ZEdWbmNtRjBhVzl1SUVOQklDMGdSek14SmpBa0JnTlZCQXNNSFVGd2NHeGxJRU5sY25ScFptbGpZWFJwYjI0Z1FYVjBhRzl5YVhSNU1STXdFUVlEVlFRS0RBcEJjSEJzWlNCSmJtTXVNUXN3Q1FZRFZRUUdFd0pWVXpBZUZ3MHlOREEwTWpreE56UTNNamRhRncweU9UQTBNamd4TnpRM01qWmFNRjh4SlRBakJnTlZCQU1NSEdWall5MXpiWEF0WW5KdmEyVnlMWE5wWjI1ZlZVTTBMVkJTVDBReEZEQVNCZ05WQkFzTUMybFBVeUJUZVhOMFpXMXpNUk13RVFZRFZRUUtEQXBCY0hCc1pTQkpibU11TVFzd0NRWURWUVFHRXdKVlV6QlpNQk1HQnlxR1NNNDlBZ0VHQ0NxR1NNNDlBd0VIQTBJQUJNSVZkKzNyMXNleUlZOW8zWENRb1NHTng3QzlieXdvUFlSZ2xkbEs5S1ZCRzROQ0R0Z1I4MEIrZ3pNZkhGVEQ5K3N5SU5hNjFkVHY5SktKaVQ1OER4T2pnZ0lSTUlJQ0RUQU1CZ05WSFJNQkFmOEVBakFBTUI4R0ExVWRJd1FZTUJhQUZDUHlTY1JQaytUdkorYkU5aWhzUDZLNy9TNUxNRVVHQ0NzR0FRVUZCd0VCQkRrd056QTFCZ2dyQmdFRkJRY3dBWVlwYUhSMGNEb3ZMMjlqYzNBdVlYQndiR1V1WTI5dEwyOWpjM0F3TkMxaGNIQnNaV0ZwWTJFek1ESXdnZ0VkQmdOVkhTQUVnZ0VVTUlJQkVEQ0NBUXdHQ1NxR1NJYjNZMlFGQVRDQi9qQ0J3d1lJS3dZQkJRVUhBZ0l3Z2JZTWdiTlNaV3hwWVc1alpTQnZiaUIwYUdseklHTmxjblJwWm1sallYUmxJR0o1SUdGdWVTQndZWEowZVNCaGMzTjFiV1Z6SUdGalkyVndkR0Z1WTJVZ2IyWWdkR2hsSUhSb1pXNGdZWEJ3YkdsallXSnNaU0J6ZEdGdVpHRnlaQ0IwWlhKdGN5QmhibVFnWTI5dVpHbDBhVzl1Y3lCdlppQjFjMlVzSUdObGNuUnBabWxqWVhSbElIQnZiR2xqZVNCaGJtUWdZMlZ5ZEdsbWFXTmhkR2x2YmlCd2NtRmpkR2xqWlNCemRHRjBaVzFsYm5SekxqQTJCZ2dyQmdFRkJRY0NBUllxYUhSMGNEb3ZMM2QzZHk1aGNIQnNaUzVqYjIwdlkyVnlkR2xtYVdOaGRHVmhkWFJvYjNKcGRIa3ZNRFFHQTFVZEh3UXRNQ3N3S2FBbm9DV0dJMmgwZEhBNkx5OWpjbXd1WVhCd2JHVXVZMjl0TDJGd2NHeGxZV2xqWVRNdVkzSnNNQjBHQTFVZERnUVdCQlNVVjl0djFYU0Job21KZGk5K1Y0VUg1NXRZSkRBT0JnTlZIUThCQWY4RUJBTUNCNEF3RHdZSktvWklodmRqWkFZZEJBSUZBREFLQmdncWhrak9QUVFEQWdOSkFEQkdBaUVBeHZBanl5WVV1ekE0aUtGaW1ENGFrL0VGYjFENmVNMjV1a3lpUWN3VTRsNENJUUMrUE5EZjBXSkg5a2xFZFRnT25VVENLS0VJa0tPaDNISkxpMHk0aUpnWXZEQ0NBdTR3Z2dKMW9BTUNBUUlDQ0VsdEw3ODZtTnFYTUFvR0NDcUdTTTQ5QkFNQ01HY3hHekFaQmdOVkJBTU1Fa0Z3Y0d4bElGSnZiM1FnUTBFZ0xTQkhNekVtTUNRR0ExVUVDd3dkUVhCd2JHVWdRMlZ5ZEdsbWFXTmhkR2x2YmlCQmRYUm9iM0pwZEhreEV6QVJCZ05WQkFvTUNrRndjR3hsSUVsdVl5NHhDekFKQmdOVkJBWVRBbFZUTUI0WERURTBNRFV3TmpJek5EWXpNRm9YRFRJNU1EVXdOakl6TkRZek1Gb3dlakV1TUN3R0ExVUVBd3dsUVhCd2JHVWdRWEJ3YkdsallYUnBiMjRnU1c1MFpXZHlZWFJwYjI0Z1EwRWdMU0JITXpFbU1DUUdBMVVFQ3d3ZFFYQndiR1VnUTJWeWRHbG1hV05oZEdsdmJpQkJkWFJvYjNKcGRIa3hFekFSQmdOVkJBb01Da0Z3Y0d4bElFbHVZeTR4Q3pBSkJnTlZCQVlUQWxWVE1Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNEUWdBRThCY1JoQm5YWklYVkdsNGxnUWQyNklDaTc5NTdyazNnamZ4TGsrRXpWdFZtV3pXdUl0Q1hkZzBpVG51NkNQMTJGODZJeTNhN1puQyt5T2dwaFA5VVJhT0I5ekNCOURCR0JnZ3JCZ0VGQlFjQkFRUTZNRGd3TmdZSUt3WUJCUVVITUFHR0ttaDBkSEE2THk5dlkzTndMbUZ3Y0d4bExtTnZiUzl2WTNOd01EUXRZWEJ3YkdWeWIyOTBZMkZuTXpBZEJnTlZIUTRFRmdRVUkvSkp4RStUNU84bjVzVDJLR3cvb3J2OUxrc3dEd1lEVlIwVEFRSC9CQVV3QXdFQi96QWZCZ05WSFNNRUdEQVdnQlM3c042aFdET0ltcVNLbWQ2K3ZldXYyc3NrcXpBM0JnTlZIUjhFTURBdU1DeWdLcUFvaGlab2RIUndPaTh2WTNKc0xtRndjR3hsTG1OdmJTOWhjSEJzWlhKdmIzUmpZV2N6TG1OeWJEQU9CZ05WSFE4QkFmOEVCQU1DQVFZd0VBWUtLb1pJaHZkalpBWUNEZ1FDQlFBd0NnWUlLb1pJemowRUF3SURad0F3WkFJd09zOXlnMUVXbWJHRyt6WERWc3Bpdi9RWDdka1BkVTJpanI3eG5JRmVRcmVKK0pqM20xbWZtTlZCRFkrZDZjTCtBakF5TGRWRUliQ2pCWGRzWGZNNE81Qm4vUmQ4TENGdGxrL0djbW1DRW05VStIcDlHNW5MbXdtSklXRUdtUThKa2gwQUFER0NBWWt3Z2dHRkFnRUJNSUdHTUhveExqQXNCZ05WQkFNTUpVRndjR3hsSUVGd2NHeHBZMkYwYVc5dUlFbHVkR1ZuY21GMGFXOXVJRU5CSUMwZ1J6TXhKakFrQmdOVkJBc01IVUZ3Y0d4bElFTmxjblJwWm1sallYUnBiMjRnUVhWMGFHOXlhWFI1TVJNd0VRWURWUVFLREFwQmNIQnNaU0JKYm1NdU1Rc3dDUVlEVlFRR0V3SlZVd0lJRm1OTWl3NHdWeGN3Q3dZSllJWklBV1VEQkFJQm9JR1RNQmdHQ1NxR1NJYjNEUUVKQXpFTEJna3Foa2lHOXcwQkJ3RXdIQVlKS29aSWh2Y05BUWtGTVE4WERUSTFNRGt3TXpBMk5UZ3pPVm93S0FZSktvWklodmNOQVFrME1Sc3dHVEFMQmdsZ2hrZ0JaUU1FQWdHaENnWUlLb1pJemowRUF3SXdMd1lKS29aSWh2Y05BUWtFTVNJRUlMNlBpSDBmbHZvbFpwR204cHorTDBFeW5lcmFuRE1VdjQ1OVNQeEJ5MFd1TUFvR0NDcUdTTTQ5QkFNQ0JFZ3dSZ0loQU0zN3k1S0prNnpIK3hydUFRT0JqcVkycmdySkNDUHZGK01YVllxSlMvMTlBaUVBOHNCR1dwVnA1SDVpVW9CeVZZWTUrVnhPd3J4bTFVMmJPU2NLelJwVUJ4SUFBQUFBQUFBPSIsImhlYWRlciI6eyJwdWJsaWNLZXlIYXNoIjoiRjM4Z01SRHdjVkVua1dDeTVNbW5NLzVJc0NQWGp4N3ByM1pTbk1ldVhiST0iLCJlcGhlbWVyYWxQdWJsaWNLZXkiOiJNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUViTjZmSE9Cd3VyWmljSUtzZVdzdkVvc0c5WHBTSzYxTVZiclovRHNEQWZ2NVJXeC9qZFJId2gzNUpwRFRzMWVUUEVkdHU3enk5NktwVExUaHVNeWwxQT09IiwidHJhbnNhY3Rpb25JZCI6IjczNzU1MDUzMWY4YjNjMjJmMmU2ODRjNzBmYzk5MzYzNDgxYjdlNDQzOTdkM2FiMDRiYWI0MTM2NjMzMWU4N2YifSwidmVyc2lvbiI6IkVDX3YxIn0=")