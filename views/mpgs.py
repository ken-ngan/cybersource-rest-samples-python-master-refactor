from flask import render_template, request, redirect, url_for, flash, session, jsonify
import datetime
from . import views
import constants

@views.route('/mpgs-c2p')
def mpgs_unified_checkout():
    session['orderId'] = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
    body = constants.mpgs_hosted_checkout.mpgs_hosted_checkout("AUTHORIZE", session['orderId'], session['amount'], session['currency'])
    session_id = body['session']['id']
    session['successIndicator'] = body['successIndicator']
    return render_template('mpgs-c2p.html', session_id=session_id)

@views.route("/mpgs-hosted-checkout", methods=["GET", "POST"])
def mpgs_hostedcheckout():
    try:
        if session.get('logged_in'):
            if request.method == "POST":
                session['orderId'] = "KN"+datetime.datetime.now().strftime("%-y%m%d%H%M%S")
                session['amount'] = request.form.get("amount")
                session['currency'] = 'HKD'
                body = constants.mpgs_hosted_checkout.mpgs_hosted_checkout("AUTHORIZE", session['orderId'], session['amount'], session['currency'])
                session['session_id'] = body['session']['id']
                session['successIndicator'] = body['successIndicator']
                return redirect(url_for('views.mpgs_hostedcheckout_confirmation'))
            else:
                return render_template("mpgs-hostedcheckout.html")
        else:
            flash("Please log in first!", category="error")
            return redirect(url_for('views.login'))
    except Exception as e:
        flash("Please log in first!", category="error")
        return redirect(url_for('views.login'))

@views.route("/mpgs-hosted-checkout-confirmation", methods=["GET", "POST"])
def mpgs_hostedcheckout_confirmation():
    return render_template("mpgs-hostedcheckout-confirmation.html", session_id=session['session_id'])

@views.route("/mpgs-receipt", methods=["GET", "POST"])
def mpgs_receipt():
    resultIndicator = request.args.get('resultIndicator')
    if resultIndicator == session['successIndicator']:
        body = constants.mpgs_retrieve_order.mpgs_retrieve_order(session['orderId'])
        return jsonify(body)
    else:
        return "Failed!"
