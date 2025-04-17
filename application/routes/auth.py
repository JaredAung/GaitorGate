from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from markupsafe import escape
import re
import MySQLdb.cursors

auth_bp = Blueprint('auth', __name__)


# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    bcrypt = current_app.config['BCRYPT']
    loginMessage = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = current_app.config['MYSQL'].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT idAccount, username, hashed_password FROM Account WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data and bcrypt.check_password_hash(user_data['hashed_password'], password):
            from app import User
            user = User.get(user_data['idAccount'])
            login_user(user)
            session['username'] = user_data['username']  # Store the username in the session
            print(f"Successfully logged in as: {session['username']}")
            return redirect(url_for('main.account')) 
             
        else:
            loginMessage = 'Incorrect username or password!'
            print('Incorrect username or password!')
                
    return render_template('login.html', loginMessage=loginMessage, title='Log In')

# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None) # Remove the username from the session
    logout_user()
    return redirect(url_for('auth.login'))

# Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    bcrypt = current_app.config['BCRYPT']
    registrationMessage = ''

    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor.execute('SELECT * FROM Account WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            registrationMessage = 'Account already exists!'
            print(registrationMessage)
        elif not username or not password or not email:
            registrationMessage = 'Please fill out the form!'
            print(registrationMessage)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            registrationMessage = 'Invalid email address!'
            print(registrationMessage)
        elif not re.match(r'^[A-Za-z0-9]{4,20}$', username):
            registrationMessage = 'Username must contain only letters and numbers!'
            print(registrationMessage)
        elif password != request.form.get('confirm_password'):
            registrationMessage = 'Passwords do not match!'
            print(registrationMessage)
        else:
            # Generate the next idUser and idAccount or need to auto increment in database schema
            cursor.execute("SELECT MAX(idUser) FROM User")
            result = cursor.fetchone()
            max_user_id = list(result.values())[0] if result else 0
            new_id_user = max_user_id + 1

            cursor.execute("SELECT MAX(idAccount) FROM Account")
            result = cursor.fetchone()
            max_account_id = list(result.values())[0] if result else 0
            new_id_account = max_account_id + 1

            # 3. Insert into User since Account has foreign key to User
            test_dob = "2000-01-01"
            cursor.execute("INSERT INTO User (idUser, name, DOB) VALUES (%s, %s, %s)", 
                (new_id_user, username, test_dob))

            # 4. Insert into Account table
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            print(f"Password: {password}")
            print(f"Hashed Password: {hashed_password}")
            cursor.execute('''
                INSERT INTO Account (idUser, idAccount, username, hashed_password, email)
                VALUES (%s, %s, %s, %s, %s)
            ''', (new_id_user, new_id_account, username, hashed_password, email))

            conn.commit()
            registrationMessage = 'You have successfully registered!'
            print(registrationMessage)

        cursor.close()

    return render_template('registration.html', registrationMessage=registrationMessage, title='Register')
