from flask import Blueprint, render_template, request, redirect, session, current_app,url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors
review_bp = Blueprint('review', __name__)

@review_bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    with current_app.app_context():
        if request.method == "POST":
            conn = current_app.config['MYSQL'].connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            index_id = request.form.get('index_id')
            review_text = request.form.get('review_text')

            cursor.execute("INSERT INTO Review (idAccount, idIndex, review_text) VALUES (%s, %s, %s)",
                           (current_user.id, index_id, review_text))
            conn.commit()
            cursor.close()
        
    return redirect(request.referrer)
    

@review_bp.route('/rating', methods=['POST'])
@login_required
def rating():
    with current_app.app_context():
        if request.method == "POST":
            conn = current_app.config['MYSQL'].connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)

            index_id = request.form.get('tool')
            rating_value = request.form.get('rating')
            print(f"Rating submitted for Index ID: {index_id} with value: {rating_value}")

            cursor.execute('Insert into Rating (rating,idIndex,idAccount) VALUES (%s,%s,%s)',
                        (rating_value, index_id, current_user.id))
            conn.commit()
            cursor.close()
    return redirect(request.referrer)
        
        
    
