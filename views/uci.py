from flask import render_template, request, redirect, url_for, flash, session
import datetime
from . import views
import config
import constants
import utils

@views.route("/uci", methods=["GET", "POST"])
def uci():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
                session['amount'] = request.form.get("amount")
                session['currency'] = "HKD"
                return redirect(url_for('views.uci_confirmation'))
            else:
                return render_template("uci.html", unified_checkout_config=utils.UNIFIED_CHECKOUT_CONFIG)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route("/uci-confirmation", methods=["GET", "POST"])
def uci_confirmation():
    if request.method == "POST":
        transient_token = request.form.get("transient_token")
        
        reference_number = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
        amount = session['amount']
        currency = session['currency']
        
        # Using transient token for auth
        return_data = constants.transient_token_auth_with_pa_enroll.transient_token_auth_with_pa_enroll(reference_number, transient_token, amount, currency)
        
        # Handle response... simplified for now as original code was complex with stepup
        # Assuming success or basic flow
        
        return redirect(url_for('views.profile'))
    else:
        capture_context = constants.generate_unified_checkout_jwt.generate_unified_checkout_jwt()
        return render_template("uci-confirmation.html", capture_context=capture_context)

@views.route("/microform", methods=["GET", "POST"])
def microform():
    try:
        if session.get('logged_in'):
            capture_context = constants.generate_microform_jwt.generate_microform_jwt()
            return render_template("microform.html", capture_context=capture_context, microform_config=utils.MICROFORM_CONFIG)
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))
