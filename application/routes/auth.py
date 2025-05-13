from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from markupsafe import escape
import re
import MySQLdb.cursors
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

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
        cursor.execute("SELECT profile_pic_url, idAccount, username, Account_Type, hashed_password, is_verified FROM Account WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data and bcrypt.check_password_hash(user_data['hashed_password'], password):
            # Comment out email verification check to allow all logins
            # if not user_data.get('is_verified', 0):
            #     loginMessage = 'Please verify your email before logging in.'
            #     print(loginMessage)
            #     return render_template('login.html', loginMessage=loginMessage, title='Log In')
            
            from app import User
            user = User.get(user_data['idAccount'])
            login_user(user)
            session['profile_pic_url'] = user_data['profile_pic_url'] 
            session['username'] = user_data['username']  
            session['Account_Type'] = user_data['Account_Type']  
            print(f"Successfully logged in as: {session['username']}")
            return redirect(url_for('main.account')) 
             
        else:
            loginMessage = 'Incorrect username or password!'
            print('Incorrect username or password!')
                
    return render_template('login.html', loginMessage=loginMessage, title='Gaitor Gate | Log In')

# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    session.pop('username', None) # Remove the username from the session
    session.pop('Account_Type', None)
    logout_user()
    return redirect(url_for('auth.login'))

# Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    bcrypt = current_app.config['BCRYPT']
    registrationMessage = ''

    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'profile_pic_url' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        profile_pic_url = request.form['profile_pic_url']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account_type = request.form.get('account_type', 'General')  
        cursor.execute('SELECT * FROM Account WHERE username = %s', (username,))
        check_username = cursor.fetchone()

        cursor.execute('SELECT * FROM Account WHERE email = %s', (email,))
        check_email = cursor.fetchone()

        if check_email:
            registrationMessage = 'Account already exists with this email!'
            print(registrationMessage)
        elif check_username:
            registrationMessage = 'Username is already taken!'
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
            try:
                # Generate the next idUser and idAccount
                cursor.execute("SELECT MAX(idUser) FROM User")
                result = cursor.fetchone()
                max_user_id = list(result.values())[0] if result else 0
                new_id_user = max_user_id + 1

                cursor.execute("SELECT MAX(idAccount) FROM Account")
                result = cursor.fetchone()
                max_account_id = list(result.values())[0] if result else 0
                new_id_account = max_account_id + 1

                # Insert into User table
                test_dob = "2000-01-01"
                cursor.execute("INSERT INTO User (idUser, name, DOB) VALUES (%s, %s, %s)", 
                    (new_id_user, username, test_dob))

                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                print(f"Password: {password}")
                print(f"Hashed Password: {hashed_password}")
                
                # Check if Account table has is_verified column
                cursor.execute("SHOW COLUMNS FROM Account LIKE 'is_verified'")
                has_is_verified = cursor.fetchone() is not None
                
                if has_is_verified:
                    print("Account table has is_verified column, using modified INSERT")
                    cursor.execute('''
                        INSERT INTO Account (profile_pic_url, idUser, idAccount, username, hashed_password, email, Account_Type, is_verified)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                    ''', (profile_pic_url, new_id_user, new_id_account, username, hashed_password, email, account_type))
                else:
                    print("Account table does NOT have is_verified column, using default INSERT")
                    cursor.execute('''
                        INSERT INTO Account (profile_pic_url, idUser, idAccount, username, hashed_password, email, Account_Type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (profile_pic_url, new_id_user, new_id_account, username, hashed_password, email, account_type))
                
                # Insert into Student table if account type is Student
                if account_type == 'Student':
                    university = request.form.get('university', 'SFSU')
                    major = request.form.get('major', '')
                    graduation_year = request.form.get('graduation_year', '')
                    # Format graduation_year as a valid date if it exists
                    if graduation_year:
                        graduation_year = f"{graduation_year}-01-01"
                    print(f"Inserting student record for account {new_id_account}: {university}, {major}, {graduation_year}")
                    cursor.execute('''
                        INSERT INTO Student (idAccount, university, major, graduation_year)
                        VALUES (%s, %s, %s, %s)
                    ''', (new_id_account, university, major, graduation_year))
                
                # Insert into Company table if account type is Company
                elif account_type == 'Company':
                    company_name = request.form.get('company_name', '')
                    website = request.form.get('website', '')
                    description = request.form.get('description', '')
                    print(f"Inserting company record for account {new_id_account}: {company_name}, {website}")
                    cursor.execute('''
                        INSERT INTO Company (idAccount, company_name, website, description)
                        VALUES (%s, %s, %s, %s)
                    ''', (new_id_account, company_name, website, description))
                
                conn.commit()
                print("User and Account records inserted successfully")
                
                # Comment out email verification sending
                # Try to send verification email
                # email_sent = send_verification_email(email, account_type)
                
                # if email_sent:
                #     registrationMessage = 'Registration successful! Please check your email to verify your account.'
                # else:
                #     registrationMessage = 'Registration successful! However, we could not send a verification email. Please contact support.'
                
                # Instead, just show registration success message
                registrationMessage = 'Registration successful! You can now log in.'
                print(registrationMessage)

            except Exception as e:
                conn.rollback()
                registrationMessage = f'Registration failed: {str(e)}'
                print(f"Registration error: {e}")

        cursor.close()

    return render_template('registration.html', registrationMessage=registrationMessage, title='Gaitor Gate | Register')

# Helper: Generate token

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except Exception:
        return False
    return email

# Helper: Send verification email

def send_verification_email(user_email, account_type=None):
    try:
        token = generate_verification_token(user_email)
        link = url_for('auth.verify_email', token=token, _external=True)
        
        # Check account type for student emails
        if account_type == 'Student' and not user_email.lower().endswith('@sfsu.edu'):
            print(f"Warning: Student account being created with non-SFSU email: {user_email}")
            # You could enforce this by returning False or raising an exception
        
        # Prepare email content
        subject = 'Verify your Gaitor Gate email'
        html_content = f'''
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; border: 1px solid #ddd; }}
                    .button {{ display: inline-block; background-color: #4CAF50; color: white; padding: 10px 20px; 
                              text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                    .footer {{ margin-top: 20px; font-size: 12px; color: #777; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header"><h2>Email Verification</h2></div>
                    <div class="content">
                        <p>Hello,</p>
                        <p>Thank you for registering with Gaitor Gate! Please click the button below to verify your email address:</p>
                        <p><a href="{link}" class="button">Verify Email</a></p>
                        <p>Or copy and paste this link into your browser:</p>
                        <p>{link}</p>
                        <p>This link will expire in 24 hours.</p>
                    </div>
                    <div class="footer">
                        <p>If you didn't register on Gaitor Gate, please ignore this email.</p>
                    </div>
                </div>
            </body>
        </html>
        '''
        
        # Send email using Flask-Mail
        print(f"Sending email via Flask-Mail to {user_email}")
        mail = current_app.config['MAIL']
        msg = Message(subject, recipients=[user_email])
        msg.html = html_content
        mail.send(msg)
        print(f"Email sent successfully to {user_email} via Flask-Mail")
        return True
            
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Email verification route
@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    print(f"Processing verification token: {token}")
    email = verify_token(token)
    if not email:
        print(f"Invalid or expired token: {token}")
        return render_template('email_verified.html', 
                            message='Invalid or expired verification link. Please try registering again.', 
                            success=False,
                            title='Verification Failed')
    
    print(f"Valid token for email: {email}")
    try:
        conn = current_app.config['MYSQL'].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if the user exists
        cursor.execute('SELECT * FROM Account WHERE email = %s', (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"No user found with email: {email}")
            return render_template('email_verified.html', 
                                message='User not found. Please register again.', 
                                success=False,
                                title='Verification Failed')
        
        # Check if Account table has is_verified column
        cursor.execute("SHOW COLUMNS FROM Account LIKE 'is_verified'")
        has_is_verified = cursor.fetchone() is not None
        
        if has_is_verified:
            print(f"Updating is_verified for email: {email}")
            cursor.execute('UPDATE Account SET is_verified = 1 WHERE email = %s', (email,))
            conn.commit()
            print(f"Successfully verified email: {email}")
            return render_template('email_verified.html', 
                                message='Your email has been verified successfully!', 
                                success=True,
                                title='Email Verified')
        else:
            print(f"is_verified column not found in Account table")
            return render_template('email_verified.html', 
                                message='Email verification feature is not properly configured.', 
                                success=False,
                                title='Verification Failed')
    
    except Exception as e:
        print(f"Error during verification: {e}")
        return render_template('email_verified.html', 
                            message=f'An error occurred during verification: {str(e)}', 
                            success=False,
                            title='Verification Error')
    finally:
        cursor.close()
