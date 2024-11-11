# routes/auth_routes.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import create_user, get_user_by_username
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        
        # Check if the user already exists
        if get_user_by_username(username):
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.signup'))
        
        # Create a new user
        create_user(username, password, email, firstname, lastname)
        flash('Signup successful! Please login.')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user_by_username(username)
        # return user
        if user and check_password_hash(user['password_hash'], password):
            # Set user in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['firstname'] = user['firstname']
            session['lastname'] = user['lastname']
            flash('Login successful!')
            return redirect(url_for('file.dashboard'))  # Redirect to dashboard or main page
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')
