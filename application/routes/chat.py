from flask import Blueprint, current_app, render_template, request
import MySQLdb.cursors
import os
from dotenv import dotenv_values
from google import genai

# take environment variablesimport os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ENV_PATH = os.path.join(BASE_DIR, "credentials", ".env")

GEMINI_KEY = dotenv_values(ENV_PATH)["GEMINI_KEY"]

chat_bp = Blueprint("chat", __name__)


def get_data():
    conn = current_app.config["MYSQL"].connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    sql = """
        select
            t.name as "AI Tool Name",
            t.description,
            c.name as category,
            group_concat(k.name) as keywords
        from SearchIndex si
        join Tools t on si.idTool = t.idTool
        left join Category c on si.idCategory = c.idCategory
        left join Keywords_Indexes ki on si.idIndex = ki.IndexId
        join Keywords k on ki.keywordID = k.idKeywords
        group by t.name, t.description, c.name;
    """
    cursor.execute(sql)
    results = cursor.fetchall()

    column_names = [x[0] for x in cursor.description]
    csv = ",".join(column_names) + "\n"
    for row in results:
        csv += ",".join([f'"{value}"' for value in row.values()]) + "\n"

    return csv


@chat_bp.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("chat.html", title="Gaitor Gate | Alli Chat")
    if request.method == "POST":
        print("post request sent")
        prompt = request.form["chat_text"]  # Changed to match the textarea name

        data = get_data()

        prompt_gemini = f"""You are a customer support chatbot for "Gaitor Gate", a search engine for AI tools. Respond using html elements to make it easier for the user to read. Answer the user's questions based ONLY on the following CSV data:

--- CSV DATA START ---
{data}
--- CSV DATA END ---

If the answer cannot be found in the CSV data, respond with "I do not have that information in the provided data." Do not use any external knowledge.

User question: {prompt}
Chatbot answer:
"""

        client = genai.Client(api_key=GEMINI_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt_gemini
        )

        return render_template(
            "chat.html",
            title="Gaitor Gate | Alli Chat",
            response=response.text,
            user_prompt=prompt,
        )

