from flask import Blueprint, render_template, request, redirect, session, current_app
from flask_login import login_required, current_user
from markupsafe import escape
import re
import MySQLdb.cursors

RESULTS_PER_PAGE = 15

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
        query_text = request.args.get("search", request.form.get("search", "")).strip()
        addToHistory(idAccount, query_text)

    with current_app.app_context():
        conn = current_app.config["MYSQL"].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        filters = request.args.getlist("filters[]")
        print("filters:", filters)
        filter_options = request.args.getlist("filter-options[]")
        print("filter options:", filter_options)
        query = request.args.get("search", request.form.get("search", "")).strip()
        page = request.args.get("page", 1, type=int)
        order_by = request.args.get("order_by", "rating")

        if not re.match(r"^[A-Za-z0-9\s]{0,40}$", query):
            # Check if the query is too long or contains invalid characters
            print("Query too long or include invalid characters")
            return render_template(
                "searchpage.html",
                data=[],
                current_page=1,
                total_pages=0,
                title="Gaitor Gate | Results",
                message="Query too long or Include Invalid Characters. Query only allow letters, numbers and spaaces",  # display error message in the front end
                search=query
            )

        filter_pairs = sorted(list(zip(filters, filter_options)))
        print(filter_pairs)

        where_clauses = []
        params = []
        # Added LIKE query for search
        for i in range(len(filters)):
            selected_filter = filters[i].strip()
            filter_option = filter_options[i].strip()

            if selected_filter == "categories" and filter_option:
                where_clauses.append("c.name = %s")
                print("category filter option:", filter_option)
                params.append(filter_option)
            elif selected_filter == "platform" and filter_option:
                where_clauses.append("p.name = %s")
                params.append(filter_option)
            elif selected_filter == "publishing date" and filter_option:
                where_clauses.append("YEAR(t.published_date) = %s")
                params.append(filter_option)

        search_condition = """
            (%s = '' OR
            LOWER(t.name) LIKE %s OR
            LOWER(t.description) LIKE %s OR
            LOWER(k.name) LIKE %s OR
            MATCH(t.name) AGAINST (%s IN NATURAL LANGUAGE MODE) OR
            MATCH(k.name) AGAINST (%s IN NATURAL LANGUAGE MODE))
        """
        where_clauses.append("(" + search_condition + ")")
        like_query = f"%{query}%"
        params.extend([query, like_query, like_query, like_query, query, query])

        order_by_statement = {
            "rating": "average_rating DESC",
            "name": "t.name",
            "date": "t.published_date DESC",
            "review": "COUNT(rv.idReview) DESC",
        }[order_by]

        sql = """
            SELECT
                si.idIndex,
                t.idTool,
                COALESCE(t.description, '') AS description, -- Use COALESCE to handle NULL descriptions
                t.name,
                Co.company_name AS company,
                t.url,
                t.thumbnail_url,
                t.published_date,
                t.pricing,
                t.version,
                c.name AS category,
                AVG(r.rating) AS average_rating
            FROM SearchIndex si
            JOIN Tools t ON si.idTool = t.idTool
            LEFT JOIN Company Co ON t.company = Co.idAccount
            LEFT JOIN Category c ON si.idCategory = c.idCategory
            LEFT JOIN IndexPlatform IP ON si.idIndex = IP.idIndex
            JOIN Platform p ON IP.idPlatform = p.idPlatform
            LEFT JOIN Keywords_Indexes ki ON ki.IndexID = si.idIndex
            LEFT JOIN Keywords k ON ki.keywordID = k.idKeywords
            LEFT JOIN Rating r ON si.idIndex = r.idIndex
            LEFT JOIN Review rv ON si.idIndex = rv.idIndex
            WHERE {}
            GROUP BY si.idIndex, t.idTool, t.description, t.name, t.company, t.url, t.thumbnail_url, t.published_date, t.pricing, t.version, c.name
            ORDER BY {}
        """.format(" AND ".join(where_clauses), order_by_statement)
        print("SQL:", sql)
        print("Params:", params)
        cursor.execute(sql, tuple(params))
        data = cursor.fetchall()
        cursor.close()

        for item in data:
            if item.get('description') is None:
                item['description'] = ''

        total_results = len(data)
        total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
        offset = (page - 1) * RESULTS_PER_PAGE
        page_data = data[offset : offset + RESULTS_PER_PAGE]

        return render_template(
            "searchpage.html",
            data=page_data,
            current_page=page,
            total_pages=total_pages,
            title="Gaitor Gate | Results",
            message="Success",
            search=query,
        )
