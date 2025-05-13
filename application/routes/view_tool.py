from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from markupsafe import escape
import re
import MySQLdb.cursors

view_tool_bp = Blueprint('view_tool',__name__)

@view_tool_bp.route('/view_tool', methods=['GET'])

def view_tool():
    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    idIndex = request.args.get('idIndex')

    #get the tool information
    cursor.execute("""
                   SELECT t.name, t.description, t.url, t.thumbnail_url, t.published_date, 
                   t.pricing, t.version, c.name as category, GROUP_CONCAT(p.name SEPARATOR ', ') as platform, si.idIndex
                   FROM SearchIndex si
                   JOIN Tools t ON si.idTool = t.idTool
                   JOIN Category c ON si.idCategory = c.idCategory
                   JOIN IndexPlatform IP ON si.idIndex = IP.idIndex
                   JOIN Platform p ON IP.idPlatform = p.idPlatform
                   WHERE si.idIndex = %s
                   """, (idIndex,))
    tool = cursor.fetchone()
    if not tool:
        return redirect(url_for('search.search'))
    
    #GET REVIEWS
    cursor.execute("""
                   SELECT r.review_text, r.created_at, a.username
                   FROM Review r
                   JOIN Account a ON a.idAccount = r.idAccount
                   WHERE r.idIndex = %s
                   ORDER BY r.created_at DESC
                   """, (idIndex,))
    reviews = cursor.fetchall()


    #GET RATING
    cursor.execute("""
                   SELECT AVG(r.rating) as average_rating,COUNT(r.idRating) as rating_count
                   FROM Rating r
                   JOIN Account ON Account.idAccount = r.idAccount
                   WHERE r.idIndex = %s
                   """, (idIndex,))
    average_rating = cursor.fetchone()
    if not average_rating or average_rating['average_rating'] is None:
        average_rating_value = 0
    else:
        average_rating_value = average_rating['average_rating']

    title = f"Gaitor Gate | {tool['name']} Info"

    print(tool, reviews, average_rating)
    cursor.close()
    return render_template('viewTool.html', title=title, item=tool, reviewdata=reviews, average_rating=average_rating_value, count = average_rating['rating_count'])