from flask import Blueprint, render_template, request, redirect, session, current_app,url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
@login_required
def history():
    conn = current_app.config["MYSQL"].connection
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM Search_History
        WHERE idAccount = %s
    """,
        (current_user.get_id(),),
    )

    data = cursor.fetchall()

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute("SELECT username, email FROM Account WHERE idAccount = %s", (current_user.id,))

    account_info = cursor.fetchone()

    title = f"{account_info['username']}'s History"

    cursor.close()

    return render_template('history.html', user=account_info, data=data, title=title)
