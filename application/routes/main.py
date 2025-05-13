from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app,
    url_for,
)
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        with current_app.app_context():
            conn = current_app.config["MYSQL"].connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            id_user = current_user.id
            # Check Users Account Type
            cursor.execute(
                "Select Account_Type FROM Account WHERE idAccount = %s", (id_user,)
            )
            account_type = cursor.fetchone()["Account_Type"]

            if account_type == "Company":
                # Display summary of Company's tool with category and platform
                cursor.execute(
                    """
                    SELECT
                        t.name,
                        t.description,
                        t.url,
                        t.thumbnail_url,
                        t.published_date,
                        t.pricing,
                        t.version,
                        c.name AS category,
                        GROUP_CONCAT(DISTINCT p.name SEPARATOR ', ') AS platforms,
                        t.idTool
                    FROM Account a
                    JOIN Company com ON a.idAccount = com.idAccount
                    JOIN Tools t ON com.idAccount = t.company
                    JOIN SearchIndex si ON t.idTool = si.idTool
                    JOIN Category c ON si.idCategory = c.idCategory
                    LEFT JOIN IndexPlatform ip ON si.idIndex = ip.idIndex
                    LEFT JOIN Platform p ON ip.idPlatform = p.idPlatform
                    WHERE a.idAccount = %s
                    GROUP BY t.idTool, c.name
                """,
                    (id_user,),
                )
                tool_summary_results = cursor.fetchall()

                # Fetch average rating for each tool in the summary
                for tool in tool_summary_results:
                    cursor.execute(
                        """
                        SELECT AVG(r.rating) AS average_rating
                        FROM Rating r
                        JOIN SearchIndex si ON r.idIndex = si.idIndex
                        JOIN Tools t ON si.idTool = t.idTool
                        WHERE t.idTool = %s
                    """,
                        (tool["idTool"],),
                    )
                    rating_data = cursor.fetchone()
                    tool["average_rating"] = (
                        rating_data["average_rating"]
                        if rating_data["average_rating"] is not None
                        else 0
                    )

                # Get reviews that were posted for this company's tools
                cursor.execute(
                    """
                    SELECT
                        t.name AS tool_name,
                        r.review_text,
                        r.created_at
                    FROM Account a
                    JOIN Company com ON a.idAccount = com.idAccount
                    JOIN Tools t ON com.idAccount = t.company
                    JOIN SearchIndex si ON t.idTool = si.idTool
                    JOIN Review r ON si.idIndex = r.idIndex
                    WHERE a.idAccount = %s
                    ORDER BY r.created_at DESC
                """,
                    (id_user,),
                )
                review_results = cursor.fetchall()
                cursor.close()
                return render_template(
                    "index.html",
                    title="Gaitor Gate | Dashboard",
                    account_type=account_type,
                    tool_summary=tool_summary_results,
                    reviews=review_results,
                )
            elif account_type in ("General", "Student"):
                # Display reviews that users posted, including the tool details
                cursor.execute(
                    """
                    SELECT
                        r.review_text,
                        t.thumbnail_url,
                        r.created_at,
                        t.name AS tool_name,
                        t.idTool
                    FROM Account a
                    JOIN Review r ON a.idAccount = r.idAccount
                    JOIN SearchIndex si ON r.idIndex = si.idIndex
                    JOIN Tools t ON si.idTool = t.idTool
                    WHERE a.idAccount = %s
                    ORDER BY r.created_at DESC
                """,
                    (id_user,),
                )
                review_results = cursor.fetchall()
                print(review_results)
                print(id_user)
                cursor.close()
                return render_template(
                    "index.html",
                    title="Gaitor Gate | Dashboard",
                    account_type=account_type,
                    tool_summary=None,
                    reviews=review_results,
                )
            else:
                return render_template("index.html", title="Gaitor Gate")
    else:
        return render_template("index.html", title="Gaitor Gate")


@main_bp.route("/about")
def about():
    return render_template("about.html", title="Gaitor Gate | About")


@main_bp.route("/members/<name>")
def team_member(name):
    title = f"Gaitor Gate | {name}'s Bio"
    return render_template(f"members/{escape(name)}.html", title=title)


@main_bp.route("/mainSearch")
def mainSearch():
    return render_template("mainSearch.html", title="Gaitor Gate | Search")


@main_bp.route("/account")
@login_required
def account():
    conn = current_app.config["MYSQL"].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT username, email, Account_Type FROM Account WHERE idAccount = %s",
        (current_user.id,),
    )
    account_info = cursor.fetchone()
    cursor.close()
    title = f"Gaitor Gate | {account_info['username']}'s Account"
    return render_template(
        "account.html", user=account_info, active_page="account", title=title
    )

