from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors

RESULTS_PER_PAGE = 8

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

    all_history_data = cursor.fetchall()
    total_results = len(all_history_data)
    total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * RESULTS_PER_PAGE
    data = all_history_data[offset : offset + RESULTS_PER_PAGE]

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT username, email FROM Account WHERE idAccount = %s", (current_user.id,))
    account_info = cursor.fetchone()

    title = f"Gaitor Gate | {account_info['username']}'s History"

    cursor.close()

    return render_template('history.html', user=account_info, data=data, title=title, current_page=page, total_pages=total_pages)

@history_bp.route("/clear_history", methods=["POST"])
@login_required
def clear_history():
    """Clear all search history for the current user"""
    conn = current_app.config["MYSQL"].connection
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "DELETE FROM Search_History WHERE idAccount = %s",
            (current_user.get_id(),)
        )
        conn.commit()
        response = {"status": "success", "message": "History cleared successfully"}
        return response, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        conn.rollback()
        response = {"status": "error", "message": str(e)}
        return response, 500, {'Content-Type': 'application/json'}
    finally:
        cursor.close()