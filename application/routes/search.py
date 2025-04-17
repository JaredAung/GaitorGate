from flask import Blueprint, render_template, request, redirect, session, current_app
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors

RESULTS_PER_PAGE = 6

search_bp = Blueprint("search", __name__)


def addToHistory(
    idAccount,
    query_text,
):
    conn = current_app.config["MYSQL"].connection
    cursor = conn.cursor()

    result = cursor.execute(
        """
        INSERT INTO Search_History
        (idAccount, query_text)
        VALUES (%s, %s)
        """,
        (idAccount, query_text),
    )

    conn.commit()
    print("result:", result)


@search_bp.route("/search", methods=["GET", "POST"])
def search():
    # add to search history if logged in
    idAccount = current_user.get_id()
    if idAccount is not None:
        query_text = request.form.get("search", "").strip()
        addToHistory(idAccount, query_text)

    with current_app.app_context():
        conn = current_app.config["MYSQL"].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        filters = request.form.getlist("filters[]")
        filter_options = request.form.getlist("filter-options[]")
        query = request.form.get("search", "").strip()
        page = request.args.get("page", 1, type=int)

        where_clauses = []
        params = []

        for i in range(len(filters)):
            selected_filter = filters[i].strip()
            filter_option = filter_options[i].strip()

            if selected_filter == "categories" and filter_option:
                where_clauses.append("c.name = %s")
                params.append(filter_option)
            elif selected_filter == "type" and filter_option:
                where_clauses.append("t.name = %s")
                params.append(filter_option)
            elif selected_filter == "publishing" and filter_option:
                where_clauses.append("YEAR(d.published_date) = %s")
                params.append(filter_option)

        search_condition = """
            %s = '' OR
            MATCH(t.name) AGAINST (%s IN NATURAL LANGUAGE MODE) OR
            MATCH(k.name) AGAINST (%s IN NATURAL LANGUAGE MODE)
        """
        where_clauses.append("(" + search_condition + ")")
        params.extend([query, query, query])

        sql = """
            
            SELECT
                si.idIndex,
                t.idTool,
                t.name,
                t.company,
                t.url,
                t.thumbnail_url,
                t.published_date,
                c.name AS category
            FROM SearchIndex si
            JOIN Tools t ON si.idTool = t.idTool
            LEFT JOIN Category c ON si.idCategory = c.idCategory
            LEFT JOIN Platform p ON si.idPlatform = p.idPlatform
            LEFT JOIN Keywords_Indexes ki ON ki.IndexID = si.idIndex
            LEFT JOIN Keywords k ON ki.keywordID = k.idKeywords
            WHERE {}
            GROUP BY si.idIndex,t.idTool, t.name, c.name;
        """.format(" AND ".join(where_clauses))

        cursor.execute(sql, tuple(params))
        data = cursor.fetchall()
        cursor.close()
        print(data)
        total_results = len(data)
        total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
        offset = (page - 1) * RESULTS_PER_PAGE
        page_data = data[offset : offset + RESULTS_PER_PAGE]

    return render_template(
        "searchpage.html",
        data=page_data,
        current_page=page,
        total_pages=total_pages,
        title="Results",
    )
