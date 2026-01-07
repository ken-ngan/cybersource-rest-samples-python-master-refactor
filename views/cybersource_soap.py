"""
CyberSource SOAP API integration views.
Handles payment processing, tokenization, and payer authentication via SOAP API.
"""
import datetime
from typing import Optional, Dict, Any, Tuple
from flask import render_template, request, redirect, url_for, flash, session
from functools import wraps
import threading
import time

from . import views
import config
import constants
from repository import TokenRepository, TransactionRepository, TempTableRepository
from utils import mask_card

# --- UTILITIES & DECORATORS ---
def login_required(f):
    """
    Decorator to require user login for protected routes.
    
    Args:
        f: Function to decorate
        
    Returns:
        Decorated function that checks login status
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@views.route("/afs")
@login_required
def afs():
    """Render AFS (Advanced Fraud Screen) page."""
    return render_template("afs.html", return_data="")

@views.route('/afs', methods=["POST"])
@login_required
def call_afs():
    """
    Call AFS service for card number.
    PCI Compliance: Card numbers must not be in URL parameters.
    Card number is received via POST request body instead.
    
    Returns:
        AFS return data
    """
    # PCI Compliance: Get card number from POST body, not URL
    card_number = request.form.get("card_number", "")
    
    if not card_number:
        flash("Card number is required", category="error")
        return redirect(url_for('views.afs'))
    
    # Security: Don't log full card numbers
    masked_card = mask_card(card_number) if len(card_number) > 4 else "****"
    
    try:
        # Process AFS request
        return_data = constants.soap_afs.afs(card_number)
        return return_data
    except Exception as e:
        flash(f"Error processing AFS request: {str(e)}", category="error")
        return redirect(url_for('views.afs'))

@views.route("/soap", methods=["GET", "POST"])
def soap():
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
                return redirect(url_for('views.soap_confirmation'))
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
                return render_template("soap.html", p=p, q=q)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        print(f"REST Error: {e}")
        return redirect(url_for('views.login'))

@views.route("/soap-confirmation", methods=["GET", "POST"])
def soap_confirmation():
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
        
        return_url = config.BASE_URL + "/views/soap-validation"
        
        try:
            # Authorization Branching
            if saved_token == "" and tokenization is None:
                return_data = constants.soap_auth_with_pa_enroll.auth_with_pa_enroll(
                    reference_number, currency , amount , card_number , exp_month , exp_year , 
                    card_type , bill_to_address_city , bill_to_address_country , bill_to_email , 
                    bill_to_phone , bill_to_forename , bill_to_surname , bill_to_address_postal_code , 
                    bill_to_address_line1, reference_id, return_url
                )

            elif saved_token == "":
                return_data = constants.soap_auth_with_pa_enroll_and_cus_token_creation.auth_with_pa_enroll_and_cus_token_creation(
                    bill_to_address_city, bill_to_address_country, bill_to_email, bill_to_phone, 
                    bill_to_forename, bill_to_surname, bill_to_address_postal_code, bill_to_address_line1, 
                    card_type, card_number, exp_month, exp_year, currency, amount, reference_number, 
                    reference_id, return_url
                )

            else:
                return_data = constants.soap_auth_with_pa_enroll_and_cus_token.auth_with_pa_enroll_and_cus_token(
                    reference_number, "authorization-with-token", currency, amount, 
                    saved_token, reference_id, return_url
                )

            if return_data and return_data.get('reasonCode') in ["475", "491"]:
                stepUpUrl = return_data.get('payerAuthEnrollReply_stepUpUrl'),
                accessToken = return_data.get('payerAuthEnrollReply_accessToken')
                return redirect(url_for('views.stepup_iframe', stepUpUrl=stepUpUrl, accessToken=accessToken, md=session_id))

            if return_data and return_data.get('reasonCode') in ["100"]:
                # ... [Handle Successful Auth Logic] ...
                flash("Transaction Successful!", "success")
                return redirect(url_for('views.profile'))
            else:
                flash(f"Declined: {getattr(return_data, 'status', 'Error')}", "error")
                return redirect(url_for('views.soap'))

        except Exception as e:
            flash("Authorization error occurred.", "error")
            return redirect(url_for('views.soap'))

    # 2. GET Phase: PA Setup
    else:
        try:
            # saved_token is now safely defined outside the POST block
            if saved_token == "":
                pay_auth_return_data = constants.soap_pa_setup_with_card_number.pa_setup_with_card_number(
                    session.get('card_number', ''),
                    session.get('exp_month', ''),
                    session.get('exp_year', '')
                )
            else:
                print("saved_token: ", saved_token)
                pay_auth_return_data = constants.soap_pa_setup_with_cus_token.pa_setup_with_cus_token(
                    saved_token
                )

            if pay_auth_return_data is None:
                flash("Payer Authentication Setup failed.", "error")
                return redirect(url_for('views.soap'))

            access_token = pay_auth_return_data.get('payerAuthSetupReply_accessToken', '')
            device_data_collection_url = pay_auth_return_data.get('payerAuthSetupReply_deviceDataCollectionURL', '')
            reference_id = pay_auth_return_data.get('payerAuthSetupReply_referenceID', '')
            session['reference_id'] = reference_id
            
            return render_template("soap-confirmation.html", access_token=access_token, device_data_collection_url=device_data_collection_url)

        except Exception as e:
            flash("Could not initialize secure authentication.", "error")
            return redirect(url_for('views.soap'))

@views.route("/soap-validation", methods=["GET", "POST"])
def soap_validation():
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
            return_data = constants.soap_auth_with_pa_valid.auth_with_pa_valid(
                reference_number, card_number, exp_month, exp_year, card_type, currency, amount, 
                bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, 
                bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id
            )
        elif saved_token == "":
            return_data = constants.soap_auth_with_pa_valid_and_cus_token_creation.auth_with_pa_valid_and_cus_token_creation(
                reference_number, card_number, exp_month, exp_year, card_type, currency, amount, 
                bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, 
                bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id
            )
            
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
            return_data = constants.soap_auth_with_pa_valid_and_cus_token.auth_with_pa_valid_and_cus_token(
                reference_number, saved_token, exp_month, exp_year, card_type, amount, currency, 
                bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, 
                bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone, transaction_id
            )
        
        id = return_data.get('requestID', '')
        eci_raw = return_data.get('payerAuthValidateReply_eciRaw', '')

        TempTableRepository.delete_temp_session(tempId)

        session['logged_in'] = True
        session['user_id'] = temp_table.get('user_id')
        session['user_email'] = temp_table.get('user_email')
        session['session_id'] = tempId

        TempTableRepository.create_temp_session(session['logged_in'], session['user_id'], session['user_email'], None, session['session_id'])

        masked_card_number = card_number[:6] + 'xxxxxx' + card_number[-4:]
        TransactionRepository.create_transaction(session['user_id'], config.MERCHANT_ID + " ("+config.ENVIRONMENT+")", reference_number, id, amount, masked_card_number, eci_raw, None, None, saved_token)
        
        # PCI Compliance: Clear sensitive data from session after processing
        # Note: CVV was never stored, so no need to clear it
        session.pop('card_number', None)

    return redirect(url_for('views.profile'))