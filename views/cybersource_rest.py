from flask import render_template, request, redirect, url_for, flash, session
import datetime
from . import views
import config
import constants
from repository import TokenRepository, TransactionRepository, TempTableRepository

@views.route("/rest", methods=["GET", "POST"])
def cybs_rest():
    try:
        if session.get('logged_in'): # Updated to match auth.py session key
            if request.method == "POST":
                session['saved_token'] = request.form.get("saved_token")
                session['exp_month'] = request.form.get("exp_month")
                session['exp_year'] = request.form.get("exp_year")
                # PCI Compliance: CVV is NEVER stored in session
                # CVV will be collected again on confirmation page if needed
                # CVV is only used during immediate API calls and never stored
                session['amount'] = request.form.get("amount")
                session['currency'] = "HKD"
                session['bill_to_forename'] = request.form.get("firstname")
                session['bill_to_surname'] = request.form.get("lastname")
                session['bill_to_address_line1'] = request.form.get("address")
                session['bill_to_address_city'] = request.form.get("city")
                session['bill_to_address_postal_code'] = request.form.get("zip")
                session['bill_to_address_country'] = request.form.get("state")
                session['bill_to_email'] = request.form.get("email")
                session['bill_to_phone'] = request.form.get("phone")
                
                session['ship_to_forename'] = request.form.get("shipto_firstname")
                session['ship_to_surname'] = request.form.get("shipto_lastname")
                session['ship_to_address'] = request.form.get("shipto_address")
                session['ship_to_address_city'] = request.form.get("shipto_city")
                session['ship_to_address_postal_code'] = request.form.get("shipto_zip")
                session['ship_to_address_country'] = request.form.get("shipto_state")
                
                session['card_type'] = request.form.get("accepted_card")
                session['card_number'] = request.form.get("card_number")
                session['tokenization'] = request.form.get("tokenization")
                return redirect(url_for('views.rest_confirmation'))
            else:
                # MIGRATION: Using Supabase dictionary structure
                user_id = session.get('user_id')
                TempTableRepository.create_temp_session(
                    session.get('logged_in'), 
                    user_id, 
                    session.get('user_email'), 
                    "", 
                    session.get('session_id')
                )
                tokens = TokenRepository.get_tokens_by_user_id(user_id)
                
                # Dictionary access instead of row[1]
                p = [row.get('payment_instrument_id') for row in tokens]
                q = [row.get('card_number') for row in tokens]
                return render_template("rest.html", p=p, q=q)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        print(f"REST Error: {e}")
        return redirect(url_for('views.login'))

@views.route("/rest-confirmation", methods=["GET", "POST"])
def rest_confirmation():
    # 1. Define variables at the start so they are available for both GET and POST
    saved_token = session.get('saved_token', "")
    session_id = session.get('session_id')
    user_id = session.get('user_id')
    
    if request.method == "POST":
        # Gather all transaction data from the session for final Auth
        # PCI Compliance: CVV is obtained from request.form, NOT from session
        reference_number = "KN" + datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        exp_month = session.get('exp_month')
        exp_year = session.get('exp_year')
        # PCI Compliance: Get CVV from request, never from session
        cvv = request.form.get("cvv", "")
        card_type = session.get('card_type')
        amount = session.get('amount')
        currency = session.get('currency')
        bill_to_forename = session.get('bill_to_forename')
        bill_to_surname = session.get('bill_to_surname')
        bill_to_address_line1 = session.get('bill_to_address_line1')
        bill_to_address_city = session.get('bill_to_address_city')
        bill_to_address_postal_code = session.get('bill_to_address_postal_code')
        bill_to_address_country = session.get('bill_to_address_country')
        bill_to_email = session.get('bill_to_email')
        bill_to_phone = session.get('bill_to_phone')
        card_number = session.get('card_number')
        tokenization = session.get('tokenization')
        reference_id = session.get('reference_id')
     
        # Sync the current state to the Supabase TempTable
        # PCI Compliance: CVV is NOT stored in temp_table
        TempTableRepository.update_temp_session(
            session_id,
            bill_to_address_line1=bill_to_address_line1, 
            bill_to_address_country=bill_to_address_country, 
            bill_to_email=bill_to_email, 
            bill_to_forename=bill_to_forename, 
            bill_to_surname=bill_to_surname, 
            bill_to_address_city=bill_to_address_city, 
            bill_to_phone=bill_to_phone, 
            bill_to_address_postal_code=bill_to_address_postal_code, 
            card_number=card_number, 
            card_type=card_type, 
            currency=currency, 
            # CVV is NOT stored in temp_table (PCI requirement)
            exp_month=exp_month, 
            exp_year=exp_year, 
            reference_id=reference_id, 
            reference_number=reference_number, 
            saved_token=saved_token, 
            tokenization=tokenization, 
            amount=amount
        )
        
        returnUrl = config.BASE_URL + "/views/rest-validation"
        
        try:
            # Authorization Branching
            if saved_token == "" and tokenization is None:
                return_data = constants.rest_auth_with_pa_enroll.rest_auth_with_pa_enroll(
                    reference_number, card_number, exp_month, exp_year, card_type, amount, 
                    currency, bill_to_forename, bill_to_surname, bill_to_address_line1, 
                    bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, 
                    bill_to_email, bill_to_phone, returnUrl, reference_id, True
                )
            elif saved_token == "":
                return_data = constants.rest_auth_with_pa_enroll_and_pi_token_creation.auth_with_pa_enroll_and_pi_token_creation(
                    reference_number, card_number, exp_month, exp_year, cvv, card_type, amount, 
                    currency, bill_to_forename, bill_to_surname, bill_to_address_line1, 
                    bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, 
                    bill_to_email, bill_to_phone, returnUrl, reference_id, False
                )
            else:
                return_data = constants.rest_auth_with_pa_enroll_and_pi_token.auth_with_pa_enroll_and_pi_token(
                    reference_number, saved_token, exp_month, exp_year, amount, currency, 
                    bill_to_forename, bill_to_surname, bill_to_address_line1, 
                    bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, 
                    bill_to_email, bill_to_phone, returnUrl, reference_id
                )

            if return_data and return_data.status == "PENDING_AUTHENTICATION":
                stepUpUrl = return_data.consumer_authentication_information.step_up_url
                accessToken = return_data.consumer_authentication_information.access_token
                return redirect(url_for('views.stepup_iframe', stepUpUrl=stepUpUrl, accessToken=accessToken, md=session_id))

            if return_data and return_data.status == "AUTHORIZED":
                # ... [Handle Successful Auth Logic] ...
                flash("Transaction Successful!", "success")
                return redirect(url_for('views.profile'))
            else:
                flash(f"Declined: {getattr(return_data, 'status', 'Error')}", "error")
                return redirect(url_for('views.cybs_rest'))

        except Exception as e:
            flash("Authorization error occurred.", "error")
            return redirect(url_for('views.cybs_rest'))

    # 2. GET Phase: PA Setup
    else:
        try:
            # saved_token is now safely defined outside the POST block
            if saved_token == "":
                pay_auth_return_data = constants.rest_pa_setup_with_card_number.rest_pa_setup_with_card_number(
                    session['card_type'], session['exp_month'], session['exp_year'], session['card_number']
                )
            else:
                print("saved_token: ", saved_token)
                pay_auth_return_data = constants.rest_pa_setup_with_pi_token.pa_setup_with_pi_token(
                    "cybs_test", saved_token
                )

            if pay_auth_return_data is None:
                flash("Payer Authentication Setup failed.", "error")
                return redirect(url_for('views.cybs_rest'))

            accessToken = pay_auth_return_data.consumer_authentication_information.access_token
            deviceDataCollectionURL = pay_auth_return_data.consumer_authentication_information.device_data_collection_url
            reference_id = pay_auth_return_data.consumer_authentication_information.reference_id
            session['reference_id'] = reference_id
            
            return render_template("rest-confirmation.html", accessToken=accessToken, deviceDataCollectionURL=deviceDataCollectionURL)

        except Exception as e:
            flash("Could not initialize secure authentication.", "error")
            return redirect(url_for('views.cybs_rest'))

@views.route("/stepup-iframe")
def stepup_iframe():
    stepUpUrl = request.args.get('stepUpUrl')
    accessToken = request.args.get('accessToken')
    md = request.args.get('md')
    return render_template("stepup-iframe.html", stepUpUrl=stepUpUrl, accessToken=accessToken, md=md)

@views.route("/rest-validation", methods=["GET", "POST"])
def rest_validation():
    if request.method == "POST":
        transaction_id = request.form.get("TransactionId")
        md = request.form.get('MD')

        temp_table = TempTableRepository.get_temp_session(md)
        if not temp_table:
            flash("Session expired or invalid", "error")
            return redirect(url_for('views.login'))
        
        tempId = temp_table.get('session_id')
        user_id = temp_table.get('user_id')
        reference_number = temp_table.get('reference_number')
        exp_month = temp_table.get('exp_month')
        exp_year = temp_table.get('exp_year')
        card_type = temp_table.get('card_type')
        amount = temp_table.get('amount')
        currency = temp_table.get('currency')
        bill_to_forename = temp_table.get('bill_to_forename')
        bill_to_surname = temp_table.get('bill_to_surname')
        bill_to_address_line1 = temp_table.get('bill_to_address_line1')
        bill_to_address_city = temp_table.get('bill_to_address_city')
        bill_to_address_postal_code = temp_table.get('bill_to_address_postal_code')
        bill_to_address_country = temp_table.get('bill_to_address_country')
        bill_to_email = temp_table.get('bill_to_email')
        bill_to_phone = temp_table.get('bill_to_phone')
        card_number = temp_table.get('card_number')
        saved_token = temp_table.get('saved_token')
        tokenization = temp_table.get('tokenization')
        
        if saved_token == "" and tokenization is None:
            return_data = constants.rest_auth_with_pa_valid.rest_auth_with_pa_valid(reference_number, card_number, exp_month, exp_year, card_type, currency, amount, bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id, True)
        elif saved_token == "":
            return_data = constants.rest_auth_with_pa_valid_and_pi_token_creation.auth_with_pa_valid_and_pi_token_creation(reference_number, card_number, exp_month, exp_year, card_type, currency, amount, bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id, False)
            # TokenRepository.create_token now handles the Supabase insert internally
            TokenRepository.create_token(
                user_id, 
                f"{config.MERCHANT_ID} ({config.ENVIRONMENT})", 
                transaction_id, 
                return_data.token_information.customer.id, 
                return_data.token_information.instrument_identifier.id, 
                card_number[:6] + 'x' * (len(card_number)-10) + card_number[-4:]
            )
        else:
            return_data = constants.rest_auth_with_pa_valid_and_pi_token.auth_with_pa_valid_and_pi_token(reference_number, saved_token, exp_month, exp_year, amount, currency, bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id)
        
        id = return_data.id
        eciRaw = return_data.consumer_authentication_information.eci_raw

        TempTableRepository.delete_temp_session(tempId)

        session['logged_in'] = True
        session['user_id'] = temp_table.get('user_id')
        session['user_email'] = temp_table.get('user_email')
        session['session_id'] = tempId

        TempTableRepository.create_temp_session(session['logged_in'], session['user_id'], session['user_email'], None, session['session_id'])

        masked_card_number = card_number[:6] + 'xxxxxx' + card_number[-4:]
        TransactionRepository.create_transaction(session['user_id'], config.MERCHANT_ID + " ("+config.ENVIRONMENT+")", reference_number, id, amount, masked_card_number, eciRaw, None, None, saved_token)
        
        # PCI Compliance: Clear sensitive data from session after processing
        # Note: CVV was never stored, so no need to clear it
        session.pop('card_number', None)

    return redirect(url_for('views.profile'))

@views.route("/token", methods=["GET", "POST"])
def profile():
    try:
        if session.get('logged_in'):
            paymentInstruments = TokenRepository.get_tokens_by_user_id(session['user_id'])
            transactions = TransactionRepository.get_transactions_by_user_id(session['user_id'])
            return render_template("token.html", paymentInstruments=paymentInstruments, transactions=transactions)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route('/processUserInfo/<string:userInfo>', methods=["GET", "POST"])
def processUserInfo(userInfo):
    customer_body = constants.retrieve_customer.retrieve_customer(userInfo)
    return customer_body

@views.route('/deleteToken/<string:tokenId>', methods=["GET", "POST"])
def deleteToken(tokenId):
    if request.method == "POST":
        token = TokenRepository.get_token_by_id(tokenId)
        if token:
            # MIGRATION: Access by key 'payment_instrument_id'
            pi_id = token.get('payment_instrument_id')
            constants.delete_customer.delete_customer(pi_id)
            TokenRepository.delete_token(tokenId)
        return redirect(url_for("views.profile"))
    
@views.route('/voidPayment/<string:id>', methods=["GET", "POST"])
def voidToken(id):
    if request.method=="POST":
        reference_number = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        transaction = TransactionRepository.get_transaction_by_id(id)
        if transaction:
            # transaction_id is at index 3 based on insert order in repository
            constants.void_payment.void_payment(reference_number, transaction[3])
        return redirect(url_for("views.profile"))

@views.route('/refundPayment/<string:id>', methods=["GET", "POST"])
def refundPayment(id):
    if request.method=="POST":
        reference_number = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        transaction = TransactionRepository.get_transaction_by_id(id)
        if transaction:
            currency = "HKD"
            # amount is at index 4, transaction_id at index 3
            constants.refund_payment.refund_payment(reference_number, transaction[4], currency, transaction[3])
        return redirect(url_for("views.profile"))

@views.route('/token/<string:reference_number>')
def transactionQuery(reference_number):
    # This returns the SDK Response Object
    api_response = constants.search_transaction.create_search_request(reference_number)
    
    # 1. Convert the SDK object to a dictionary
    # Most CyberSource SDK objects support .to_dict()
    if hasattr(api_response, 'to_dict'):
        search_results = api_response.to_dict()
    else:
        # Fallback if it's already a dict or something else
        search_results = api_response

    # 2. Now you can safely check 'embedded' in the dictionary
    if search_results and 'embedded' in search_results:
        # The key in the SDK dict might be 'embedded' or '_embedded' 
        # based on the specific version of the client.
        embedded_data = search_results.get('embedded') or search_results.get('_embedded')
        
        if embedded_data:
            summaries = embedded_data.get('transaction_summaries', [])
            if summaries:
                # Pick the last transaction (the Authorization)
                transaction_data = summaries[-1]
                return render_template("transaction-details.html", return_data=transaction_data)
    
    flash("No transaction details found for this reference.", "error")
    return redirect(url_for('views.profile'))

@views.route("/report")
def report():
    try:
        if session.get('logged_in'):
            return render_template("report.html", return_data="")
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
       flash("Please log in first!", category="error")
       return redirect(url_for('views.login'))

@views.route("/report", methods=["GET", "POST"])
def gen_report():
    startTime = request.form.get("startTime")+"T00:00:00.000Z"
    endTime = request.form.get("endTime")+"T00:00:00.000Z"
    timeQueryType = request.form.get("timeQueryType")
    reportMimeType = request.form.get("reportMimeType")

    return_data = constants.query_report.retrieve_available_reports(startTime, endTime, timeQueryType, reportMimeType)
    return render_template("report.html", return_data=return_data)

@views.route('/downloadReport/<string:id>', methods=["GET", "POST"])
def downloadReport(id):
    if request.method=="POST":
        return_data = constants.retrieve_report.get_report_based_on_report_id(id)
        reportDate = return_data.report_end_time.strftime("%Y-%m-%d")
        reportName = return_data.report_name
        reportMimeType = return_data.report_mime_type
        constants.download_report.download_report(reportDate, reportName, reportMimeType)
        return redirect(url_for('views.gen_report'))
