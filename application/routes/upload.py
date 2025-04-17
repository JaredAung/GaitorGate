from flask import Blueprint, render_template, request, redirect, session, current_app,url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/dataUpload', methods=['GET', 'POST'])
@login_required
def dataUpload():
    uploadMessage = ''
    with current_app.app_context():  # <-- Add this context manager
        if request.method == "POST":
            conn = mysql.connection  # <-- Establish connection
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
