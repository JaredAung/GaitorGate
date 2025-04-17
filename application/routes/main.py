from flask import Blueprint, render_template, request, redirect, session, current_app,url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template("index.html", data=[], current_page=1, total_pages=0, title='Gaitor Gate')

@main_bp.route('/about')
def about():
    return render_template("about.html", title='About')

@main_bp.route('/members/<name>')
def team_member(name):
    return render_template(f"members/{escape(name)}.html", title=name)

@main_bp.route('/dataUpload', methods=['GET', 'POST'])
@login_required
def dataUpload():
    uploadMessage = ''
    with current_app.app_context():  
        if request.method == "POST":
            conn = mysql.connection 
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            name = request.form['name']
            company = request.form['company']
            url = request.form['url']
            thumbnailUrl = request.form['thumbnail']
            version = request.form['version']
            pricing = request.form['pricing']

            cursor.execute('SELECT * FROM Tools WHERE name = %s', (name,))
            tool = cursor.fetchone()
            if tool:
                uploadMessage = "Tool already exists"
                print(uploadMessage)
            else:
                cursor.execute("INSERT INTO Tools (name, company, url, thumbnail, " \
                "version, pricing) Values (%s, %s)", (name, company, url, thumbnailUrl, version, pricing))
                conn.commit()
                print(uploadMessage)
                return redirect("dataUpload.html", uploadMessage=uploadMessage)
        return render_template('dataUpload.html', title='Upload')

# Repurposed Temporarily to act as main page for new search
@main_bp.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", title='Search')

@main_bp.route('/account')
@login_required
def account():
    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT username, email FROM Account WHERE idAccount = %s", (current_user.id,))
    account_info = cursor.fetchone()
    cursor.close()
    title = f"{account_info['username']}'s Account"
    return render_template('account.html', user=account_info, active_page='account', title=title)

@main_bp.route('/saved')
@login_required
def saved():
    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT username, email FROM Account WHERE idAccount = %s", (current_user.id,))
    account_info = cursor.fetchone()
    cursor.close()
    title = f"{account_info['username']}'s Saved"
    return render_template('saved.html', user=account_info, title=title)

# Repurposed Temporarily to act as main page for new search
@main_bp.route('/settings')
def settings():
    return render_template("settings.html", title='Settings')
