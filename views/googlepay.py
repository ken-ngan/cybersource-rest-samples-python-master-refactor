from flask import render_template, request, redirect, url_for, flash, session
import datetime
import json
from . import views
import config
import constants
from repository import TokenRepository, TransactionRepository, TempTableRepository

@views.route("/googlepay", methods=["GET", "POST"])
def googlepay():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
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
                
                return redirect(url_for('views.googlepay_confirmation'))
            else:
                return render_template("googlepay.html")
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route("/googlepay-confirmation", methods=["GET", "POST"])
def googlepay_confirmation():
    if request.method == "POST":
        googlepay_token = request.form.get("googlepay_token")
        
        reference_number = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        amount = session['amount']
        currency = session['currency']
        bill_to_forename = session['bill_to_forename']
        bill_to_surname = session['bill_to_surname']
        bill_to_address_line1 = session['bill_to_address_line1']
        bill_to_address_city = session['bill_to_address_city']
        bill_to_address_postal_code = session['bill_to_address_postal_code']
        bill_to_address_country = session['bill_to_address_country']
        bill_to_email = session['bill_to_email']
        bill_to_phone = session['bill_to_phone']
        
        # REST API Google Pay
        # return_data = constants.rest_google_pay_auth.google_pay_auth(reference_number, googlepay_token, amount, currency, bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone)
        # transaction_id = return_data.id
        
        # SOAP API Google Pay
        return_data = constants.soap_google_pay_auth.google_pay_auth(reference_number, googlepay_token, amount, currency, bill_to_forename, bill_to_surname, bill_to_address_line1, bill_to_address_city, bill_to_address_postal_code, bill_to_address_country, bill_to_email, bill_to_phone)
        transaction_id = return_data['requestID']
        decision = return_data['decision']
        reason_code = return_data['reasonCode']
        
        TransactionRepository.create_transaction(session['user_id'], config.MERCHANT_ID + " ("+config.ENVIRONMENT+")", reference_number, transaction_id, amount, "Google Pay", None, decision, reason_code)
        
        return redirect(url_for('views.profile'))
    else:
        # Setup for Google Pay Payer Auth if needed, but here just rendering confirmation
        return render_template("googlepay-confirmation.html", merchantId=config.MERCHANT_ID)
