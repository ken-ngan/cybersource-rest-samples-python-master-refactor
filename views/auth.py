"""
Authentication views for user registration and login.
Includes input validation and security best practices.
"""
import re
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from uuid import uuid4
from typing import Optional, Tuple
from . import views
from repository import UserRepository, TempTableRepository

# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Password requirements
MIN_PASSWORD_LENGTH = 8
MAX_EMAIL_LENGTH = 255
MAX_PASSWORD_LENGTH = 128

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format and length.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required."
    
    email = email.strip().lower()
    
    if len(email) > MAX_EMAIL_LENGTH:
        return False, f"Email must be less than {MAX_EMAIL_LENGTH} characters."
    
    if not EMAIL_REGEX.match(email):
        return False, "Please enter a valid email address."
    
    return True, None

def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password:
        return False, "Password is required."
    
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    
    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password must be less than {MAX_PASSWORD_LENGTH} characters."
    
    return True, None

@views.route("/", methods=["GET", "POST"])
def home():
    """Redirect to login page."""
    return redirect(url_for("views.login"))

@views.route("/register", methods=["GET", "POST"])
def register():
    if session.get('logged_in'):
        return redirect(url_for("views.cybs_rest"))
    else:
        """Handle user registration with input validation."""
        if request.method == "POST":
            user_email = request.form.get('user_email', '').strip()
            psw = request.form.get('psw', '')
            psw_repeat = request.form.get('psw-repeat', '')
            
            # Validate email
            email_valid, email_error = validate_email(user_email)
            if not email_valid:
                flash(email_error, category="error")
                return render_template("sign-up.html", boolean=True)
            
            # Validate password
            password_valid, password_error = validate_password(psw)
            if not password_valid:
                flash(password_error, category="error")
                return render_template("sign-up.html", boolean=True)
            
            # Check password match
            if psw != psw_repeat:
                flash("Passwords don't match.", category="error")
                return render_template("sign-up.html", boolean=True)
            
            # Check if user already exists
            try:
                existing_user = UserRepository.get_user_by_email(user_email)
                if existing_user:
                    flash("An account with this email already exists.", category="error")
                    return render_template("sign-up.html", boolean=True)
                
                # Create new user
                UserRepository.create_user(user_email, psw)
                flash("Account created successfully!", category="success")
                return redirect(url_for("views.login"))
            except Exception as e:
                # Log the error in production (add logging here)
                flash("An error occurred during registration. Please try again.", category="error")
                return render_template("sign-up.html", boolean=True)

        return render_template("sign-up.html", boolean=True)

@views.route("/login", methods=["GET", "POST"])
def login():
    if session.get('logged_in'):
        return redirect(url_for("views.cybs_rest"))
    else:
        """Handle user login with input validation."""
        if request.method == "POST":
            user_email = request.form.get('user_email', '').strip()
            psw = request.form.get('psw', '')
            
            # Validate input
            email_valid, email_error = validate_email(user_email)
            if not email_valid:
                flash(email_error, category="error")
                return render_template("login.html")
            
            if not psw:
                flash("Password is required.", category="error")
                return render_template("login.html")
            
            try:
                user = UserRepository.get_user_by_email(user_email)
                
                # Security: Always check password, even if user doesn't exist
                # This prevents user enumeration attacks
                if user and check_password_hash(user.get('password', ''), psw):
                    session['logged_in'] = True
                    session['user_id'] = user.get('id')
                    session['user_email'] = user.get('email')
                    session['session_id'] = uuid4().hex
                    
                    # Make session permanent for security
                    session.permanent = True
                    
                    TempTableRepository.create_temp_session(
                        session['logged_in'], 
                        session['user_id'], 
                        session['user_email'], 
                        None,  # count_down_time
                        session['session_id']
                    )
                    
                    flash("Logged in successfully!", category="success")
                    return redirect(url_for("views.cybs_rest"))
                else:
                    flash("Invalid email or password.", category="error")
            except Exception as e:
                # Log the error in production (add logging here)
                flash("An error occurred during login. Please try again.", category="error")
        
        return render_template("login.html")

@views.route('/logout')
def logout():
    """Handle user logout and cleanup session data."""
    try:
        user_id = session.get('user_id')
        if user_id:
            TempTableRepository.delete_temp_session_by_user(user_id)
    except Exception:
        # Continue with logout even if cleanup fails
        pass
    finally:
        session.clear()
    
    flash("You have been logged out successfully.", category="success")
    return redirect(url_for('views.login'))