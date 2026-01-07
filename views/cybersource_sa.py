from flask import render_template, request, redirect, url_for, flash, session
import datetime
from uuid import uuid4
from . import views
import config
import utils
from repository import TokenRepository, TransactionRepository, TempTableRepository

@views.route("/secure-acceptance", methods=["GET", "POST"])
def secure_acceptance():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
                # ... [Session data storage remains the same] ...
                session['amount'] = request.form.get("amount")
                session['bill_to_forename'] = request.form.get("bill_to_forename")
                session['bill_to_surname'] = request.form.get("bill_to_surname")
                session['bill_to_email'] = request.form.get("bill_to_email")
                session['bill_to_address_line1'] = request.form.get("bill_to_address_line1")
                session['bill_to_address_city'] = request.form.get("bill_to_address_city")
                session['bill_to_address_country'] = request.form.get("bill_to_address_country")
                session['bill_to_address_postal_code'] = request.form.get("bill_to_address_postal_code")
                session['bill_to_phone'] = request.form.get("bill_to_phone")
                session['locale'] = 'zh-hk'
                session['currency'] = 'HKD'
                session['transaction_type'] = request.form.get("transaction_type")
                session['payment_token'] = request.form.get("saved_token")
                return redirect(url_for('views.secure_acceptance_confirmation'))
            else:
                tokens = TokenRepository.get_tokens_by_user_id(session['user_id'])
                
                # MIGRATION UPDATE: tokens is now a list of dictionaries.
                # Use keys instead of numeric indices row[1] and row[2].
                p = [row.get('payment_instrument_id') for row in tokens]
                q = [row.get('card_number') for row in tokens]
                
                return render_template("secure-acceptance.html", p=p, q=q)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        print(f"Secure Acceptance Error: {e}")
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route("/secure-acceptance-confirmation", methods=["GET", "POST"])
def secure_acceptance_confirmation():
    if request.method == "POST":
        session['transaction_uuid'] = uuid4().hex
        session['reference_number'] = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        
        fields = {}
        fields['profile_id'] = config.SA_PROFILE_ID
        fields['access_key'] = config.SA_ACCESS_KEY
        fields['amount'] = session['amount']
        fields['transaction_uuid'] = session['transaction_uuid']
        fields['bill_to_forename'] = session['bill_to_forename']
        fields['bill_to_surname'] = session['bill_to_surname']
        fields['bill_to_email'] = session['bill_to_email']
        fields['bill_to_address_line1'] = session['bill_to_address_line1']
        fields['bill_to_address_city'] = session['bill_to_address_city']
        fields['bill_to_address_country'] = session['bill_to_address_country']
        fields['bill_to_address_postal_code'] = session['bill_to_address_postal_code']
        fields['bill_to_phone'] = session['bill_to_phone']
        fields['locale'] = session['locale']
        fields['currency'] = session['currency']
        fields['transaction_type'] = session['transaction_type']
        fields['reference_number'] = session['reference_number']
        fields['auth_trans_ref_no'] = session['reference_number']
        fields['payment_token'] = session['payment_token']
        
        if "update_payment_token" in session['transaction_type']:
            fields['allow_payment_token_update'] = "true"
        
        fields['override_custom_receipt_page']= config.BASE_URL + '/views/secure-acceptance-receipt'
        
        context =  {}
        if fields['transaction_type'] == "create_payment_token":
            signed_context = utils.sign_fields_to_context(fields, context, config.SA_SECRET_KEY, config.SA_CREATE_TOKEN_URL)
        elif fields['transaction_type'] == "update_payment_token":
            signed_context = utils.sign_fields_to_context(fields, context, config.SA_SECRET_KEY, config.SA_UPDATE_TOKEN_URL)
        else:
            signed_context = utils.sign_fields_to_context(fields, context, config.SA_SECRET_KEY, config.SA_URL)   
        
        return render_template("post_to_cybersource.html", url=signed_context['url'], fields=signed_context['fields'], signature=signed_context['signature'])
    else:
        return render_template("secure-acceptance-confirmation.html")

@views.route("/secure-acceptance-receipt", methods=["GET", "POST"])
def secure_acceptance_receipt():
    # ... [Retrieving form data remains the same] ...
    payment_token = request.form.get("payment_token")
    decision = request.form.get("decision")
    reason_code = request.form.get("reason_code")
    amount = request.form.get('auth_amount')
    eci_raw = request.form.get('payer_authentication_eci')
    transaction_id = request.form.get("transaction_id")
    req_card_number = request.form.get("req_card_number")
    reference_number = request.form.get("req_reference_number")

    user_id = session.get('user_id')
    
    if payment_token:
        payment_token_instrument_identifier_id = request.form.get("payment_token_instrument_identifier_id")
        # TokenRepository.create_token now handles the Supabase insert internally
        TokenRepository.create_token(
            user_id, 
            f"{config.MERCHANT_ID} ({config.ENVIRONMENT})", 
            transaction_id, 
            payment_token, 
            payment_token_instrument_identifier_id, 
            req_card_number
        )
    
    TransactionRepository.create_transaction(
        user_id, 
        f"{config.MERCHANT_ID} ({config.ENVIRONMENT})", 
        reference_number, 
        transaction_id, 
        amount, 
        req_card_number, 
        eci_raw, 
        decision, 
        reason_code
    )
    
    TempTableRepository.delete_temp_session_by_user(user_id)
    return render_template("secure-acceptance-receipt.html")

@views.route("/android-secure-acceptance-confirmation", methods=["GET", "POST"])
def android_secure_acceptance_confirmation():
        session['transaction_uuid'] = uuid4().hex
        session['reference_number'] = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        
        fields = {}
        fields['profile_id'] = config.SA_PROFILE_ID
        fields['access_key'] = config.SA_ACCESS_KEY
        fields['amount'] = '123.45'
        fields['transaction_uuid'] = session['transaction_uuid']
        fields['bill_to_forename'] = 'John'
        fields['bill_to_surname'] = 'Doe'
        fields['bill_to_email'] = 'john.doe@globalpay.com'
        fields['bill_to_address_line1'] = '27/F, Manhattan Place,'
        fields['bill_to_address_city'] = 'Kowloon Bay,'
        fields['bill_to_address_country'] = 'HK'
        fields['bill_to_address_postal_code'] = '00000'
        fields['bill_to_phone'] = '35293565'
        fields['locale'] = 'CA'
        fields['currency'] = 'HKD'
        fields['transaction_type'] = 'authorization'
        fields['reference_number'] = session['reference_number']
        fields['payment_token'] = ''
        fields['override_custom_receipt_page']= config.BASE_URL + 'views/android-secure-acceptance-receipt'
        context =  {}
        signed_context = utils.sign_fields_to_context(fields, context, config.SA_SECRET_KEY, config.SA_URL)
        
        return render_template("android_post_to_cybersource.html", url=signed_context['url'], fields=signed_context['fields'], signature=signed_context['signature'])

@views.route("/android-secure-acceptance-receipt", methods=["GET", "POST"])
def android_secure_acceptance_receipt():
    payment_token = request.form.get("payment_token")
    if payment_token is not None:
        user_id = session['user_id']
        transaction_id = request.form.get("transaction_id")
        payment_token_instrument_identifier_id = request.form.get("payment_token_instrument_identifier_id")
        req_card_number = request.form.get("req_card_number").upper()
        
        TokenRepository.create_token(user_id, config.MERCHANT_ID + " ("+config.ENVIRONMENT+")", transaction_id, payment_token, payment_token_instrument_identifier_id, req_card_number)
    
    return render_template("android-secure-acceptance-receipt.html")

@views.route("/sop", methods=["GET", "POST"])
def sop():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
                # ... [Session data storage remains the same] ...
                session['reference_number'] = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
                session['amount'] = request.form.get("amount")
                session['bill_to_forename'] = request.form.get("bill_to_forename")
                session['bill_to_surname'] = request.form.get("bill_to_surname")
                session['bill_to_email'] = request.form.get("bill_to_email")
                session['bill_to_address_line1'] = request.form.get("bill_to_address_line1")
                session['bill_to_address_city'] = request.form.get("bill_to_address_city")
                session['bill_to_address_country'] = request.form.get("bill_to_address_country")
                session['bill_to_address_postal_code'] = request.form.get("bill_to_address_postal_code")
                session['bill_to_phone'] = request.form.get("bill_to_phone")
                session['locale'] = 'en-us'
                session['currency'] = 'HKD'
                session['transaction_type'] = request.form.get("transaction_type")
                session['payment_token'] = request.form.get("saved_token")
                return redirect(url_for('views.sop_confirmation'))
            else:
                tokens = TokenRepository.get_tokens_by_user_id(session['user_id'])
                
                # MIGRATION UPDATE: tokens is now a list of dictionaries.
                p = [row.get('payment_instrument_id') for row in tokens]
                q = [row.get('card_number') for row in tokens]
                
                return render_template("sop.html", p=p, q=q)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        print(f"SOP Error: {e}")
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route("/sop-confirmation", methods=["GET", "POST"])
def sop_confirmation():
    if request.method == "POST":
        session['transaction_uuid'] = uuid4().hex
        
        fields = {}
        fields['profile_id'] = config.SOP_PROFILE_ID
        fields['access_key'] = config.SOP_ACCESS_KEY
        fields['amount'] = session['amount']
        fields['transaction_uuid'] = session['transaction_uuid']
        fields['bill_to_forename'] = session['bill_to_forename']
        fields['bill_to_surname'] = session['bill_to_surname']
        fields['bill_to_email'] = session['bill_to_email']
        fields['bill_to_address_line1'] = session['bill_to_address_line1']
        fields['bill_to_address_city'] = session['bill_to_address_city']
        fields['bill_to_address_country'] = session['bill_to_address_country']
        fields['bill_to_address_postal_code'] = session['bill_to_address_postal_code']
        fields['bill_to_phone'] = session['bill_to_phone']
        fields['locale'] = session['locale']
        fields['currency'] = session['currency']
        fields['transaction_type'] = session['transaction_type']
        fields['reference_number'] = session['reference_number']
        fields['auth_trans_ref_no'] = session['reference_number']
        if session['payment_token'] is not None:
            fields['payment_token'] = session['payment_token']
        fields['payment_method'] = 'card'
        fields['override_custom_receipt_page']= config.BASE_URL + '/views/secure-acceptance-receipt'
        context =  {}
        
        if session['payment_token'] is None:
            signed_context = utils.sop_sign_fields_to_context(fields, context, config.SOP_SECRET_KEY, config.SOP_URL)
            return render_template("secure_payment_form.html", url=signed_context['url'], fields=signed_context['fields'], signature=signed_context['signature'])
        else:
            signed_context = utils.sign_fields_to_context(fields, context, config.SOP_SECRET_KEY, config.SOP_URL)
            return render_template("post_to_cybersource.html", url=signed_context['url'], fields=signed_context['fields'], signature=signed_context['signature'])
    else:
        return render_template("sop-confirmation.html")
