from flask import render_template, request, redirect, url_for, flash, session
import datetime, time
import uuid
from . import views
import config
import utils
from repository import TokenRepository, TempTableRepository, TransactionRepository

@views.route("/ticketing", methods=["GET", "POST"])
def ticketing():
    try:
        # Standardized with auth.py: session['logged_in']
        if session.get('logged_in'):
            if request.method == "POST":
                session['reference_number'] = "KN" + datetime.datetime.now().strftime("%-y%m%d%H%M%S")
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
                session['accepted_offer'] = request.form.get("accepted_offer")
                session['payment_token'] = request.form.get("saved_token")
                return redirect(url_for('views.ticketing_tnc_overlay'))
            else:
                # Standardized with auth.py: session['user_id']
                user_id = session.get('user_id')
                tokens = TokenRepository.get_tokens_by_user_id(user_id)

                session_id = session.get('session_id')
                count_down_time = int(time.mktime(datetime.datetime.now().timetuple())) * 1000
                session['count_down_time'] = count_down_time
                
                data = {"count_down_time": count_down_time}
                TempTableRepository.update_temp_session(session_id, **data)

                # Supabase dictionary mapping
                p = [row.get('payment_instrument_id') for row in tokens]
                q = [row.get('card_number') for row in tokens]
                return render_template("/ticketing/ticketing_checkout_overlay.html", count_down_time=count_down_time, p=p, q=q)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        print(f"Ticketing Route Error: {e}")
        flash("An error occurred. Please log in again.", category="error")
        return redirect(url_for('views.login'))

@views.route("/ticketing-tnc-overlay", methods=["GET", "POST"])
def ticketing_tnc_overlay():
    session['transaction_uuid'] = uuid.uuid4().hex
    
    fields = {
        'profile_id': config.SOP_PROFILE_ID,
        'access_key': config.SOP_ACCESS_KEY,
        'amount': session.get('amount'),
        'transaction_uuid': session.get('transaction_uuid'),
        'bill_to_forename': session.get('bill_to_forename'),
        'bill_to_surname': session.get('bill_to_surname'),
        'bill_to_email': session.get('bill_to_email'),
        'bill_to_address_line1': session.get('bill_to_address_line1'),
        'bill_to_address_city': session.get('bill_to_address_city'),
        'bill_to_address_country': session.get('bill_to_address_country'),
        'bill_to_address_postal_code': session.get('bill_to_address_postal_code'),
        'bill_to_phone': session.get('bill_to_phone'),
        'locale': session.get('locale'),
        'currency': session.get('currency'),
        'transaction_type': "authorization",
        'reference_number': session.get('reference_number'),
        'auth_trans_ref_no': session.get('reference_number'),
        'payment_method': 'card',
        'override_custom_receipt_page': config.BASE_URL + '/views/ticketing-confirmation-overlay'
    }
    
    signed_context = utils.sop_sign_fields_to_context(fields, {}, config.SOP_SECRET_KEY, config.SOP_URL)
    
    # Update temporary session with offer and reference
    session_id = session.get('session_id')
    data = {
        "reference_number": session.get('reference_number'),
        "accepted_offer": session.get('accepted_offer')
    }
    TempTableRepository.update_temp_session(session_id, **data)
    
    return render_template("ticketing/ticketing_tnc_overlay.html", 
                           count_down_time=session.get('count_down_time'), 
                           reference_number=session.get('reference_number'), 
                           url=signed_context['url'], 
                           fields=signed_context['fields'], 
                           signature=signed_context['signature'], 
                           override_custom_receipt_page=fields['override_custom_receipt_page'])

@views.route("/ticketing-confirmation-overlay", methods=["GET", "POST"])
def ticketing_confirmation_overlay():
    # Capture response from CyberSource Secure Acceptance
    decision = request.form.get("decision")
    reason_code = request.form.get("reason_code")
    amount = request.form.get('auth_amount')
    eciRaw = request.form.get('payer_authentication_eci')
    transaction_id = request.form.get("transaction_id")
    req_card_number = request.form.get("req_card_number")
    reference_number = request.form.get("req_reference_number")
    
    # 1. Fetch temp session from Supabase using the reference number
    temp_session = TempTableRepository.get_temp_session_by_reference(reference_number)
    
    if temp_session:
        user_id = temp_session.get('user_id')
        mid_label = f"{config.MERCHANT_ID} ({config.ENVIRONMENT})"
        
        # 2. Log transaction into Supabase
        TransactionRepository.create_transaction(
            user_id, mid_label, reference_number, transaction_id, 
            amount, req_card_number, eciRaw, decision, reason_code, 
            session.get('payment_token', "")
        )
        
        # 3. Cleanup temp session
        TempTableRepository.delete_temp_session_by_user(user_id)
        
    return render_template("ticketing/ticketing_confirmation_overlay.html")

@views.route("/ticketing-receipt-overlay/<string:reference_number>", methods=["GET", "POST"])
def ticketing_receipt_overlay(reference_number):
    user_id = session.get('user_id')
    # Fetch transactions from Supabase
    transactions = TransactionRepository.get_transaction_by_reference(user_id, reference_number)
    print("transactions: ", transactions)
    return render_template("ticketing/ticketing_receipt_overlay.html", transactions=transactions)

@views.route("/ticketing-timeout", methods=["GET"])
def ticketing_timeout():
    return render_template("ticketing/ticketing_timeout.html")