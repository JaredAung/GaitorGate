from flask import Blueprint, render_template, request, redirect, session, current_app,url_for
from flask_login import login_required, current_user
from markupsafe import escape
import MySQLdb.cursors
upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/dataUpload', methods=['GET', 'POST'])
@login_required
def dataUpload():
    with current_app.app_context():  # <-- Add this context manager
        upload_message = ""
        if request.method == "POST":
            conn = current_app.config['MYSQL'].connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            # Get input from user
            name = request.form['name']
            company = current_user.id
            #companyID = current_user.id
            url = request.form['url']
            thumbnailUrl = request.form['thumbnailUrl']
            version = request.form['version']
            if not version: version = 1.0
            pricing = request.form['pricing']
            if not pricing: pricing = 0.00
            
            platform_values = [v for k, v in request.form.items() if k.startswith("platform")]
            print("Detected platforms:", platform_values)
            category = request.form['category']

            description = request.form['description']
            cursor.execute('SELECT * FROM Tools WHERE name = %s', (name,))
            tool_name = cursor.fetchone()
            # Check if tool already exists
            if tool_name:
                upload_message = "Tool already exists"
                print(upload_message)
            else:
                cursor.execute("INSERT INTO Tools (name, company, url, thumbnail_url, " \
                "version, pricing,description) Values (%s, %s, %s, %s, %s, %s,%s)", 
                (name, company, url, thumbnailUrl, version, pricing,description)) # ADD DESCRIPTION ONCE FRONTEND ADDS TO FORM
                toolId = cursor.lastrowid
                cursor.execute("Select idCategory FROM Category WHERE name = %s", (category,))
                categoryId = cursor.fetchone()['idCategory']
                
                cursor.execute("""INSERT INTO SearchIndex (idTool, idCategory) 
                               Values(%s, %s)""", 
                               (toolId, categoryId))
                conn.commit()
                indexId = cursor.lastrowid

                for platform in platform_values:
                    cursor.execute("Select idPlatform FROM Platform WHERE name = %s",(platform,))
                    platformId = cursor.fetchone()['idPlatform']
                    cursor.execute(""" INSERT INTO IndexPlatform (idIndex, idPlatform) VALUES (%s,%s)""",
                               (indexId, platformId))
                    conn.commit()

                upload_message = "Tool successfully uploaded."
                print(upload_message)
                #return redirect("dataUpload.html", uploadMessage=uploadMessage)
        return render_template('dataUpload.html', title='Gaitor Gate | Upload', uploadMessage=upload_message)

@upload_bp.route('/dataUpdate', methods=['GET', 'POST'])
@login_required
def dataUpdate():
    with current_app.app_context():
        update_message = ""
        if request.method == "POST":
            conn = current_app.config['MYSQL'].connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            tool_name_from_form = request.form.get('name')
            company_id = current_user.id

            # Get input from user
            name = request.form['name']
            url = request.form['url']
            thumbnailUrl = request.form['thumbnailUrl']
            version = request.form['version']
            if not version: version = 1.0
            pricing = request.form['pricing']
            if not pricing: pricing = 0.00

            platform_values = [v for k, v in request.form.items() if k.startswith("platform")]
            print("Detected platforms:", platform_values)
            category = request.form['category']
            description = request.form['description']

            # Find the tool ID based on name and company ID
            cursor.execute("SELECT idTool FROM Tools WHERE name = %s AND company = %s", (tool_name_from_form, company_id))
            tool_data = cursor.fetchone()

            if tool_data:
                tool_id = tool_data['idTool']
                # Update the Tools table
                cursor.execute("""
                    UPDATE Tools
                    SET name = %s, url = %s, thumbnail_url = %s,
                        version = %s, pricing = %s, description = %s
                    WHERE idTool = %s
                """, (name, url, thumbnailUrl, version, pricing, description, tool_id))

                # Update the Category in SearchIndex
                cursor.execute("SELECT idCategory FROM Category WHERE name = %s", (category,))
                category_id = cursor.fetchone()['idCategory']
                cursor.execute("""
                    UPDATE SearchIndex
                    SET idCategory = %s
                    WHERE idTool = %s
                """, (category_id, tool_id))

                # Update Platforms in IndexPlatform
                cursor.execute("SELECT idIndex FROM SearchIndex WHERE idTool = %s", (tool_id,))
                index_id = cursor.fetchone()['idIndex']
                cursor.execute("DELETE FROM IndexPlatform WHERE idIndex = %s", (index_id,))
                for platform in platform_values:
                    cursor.execute("SELECT idPlatform FROM Platform WHERE name = %s", (platform,))
                    platform_id = cursor.fetchone()['idPlatform']
                    cursor.execute("INSERT INTO IndexPlatform (idIndex, idPlatform) VALUES(%s, %s)", (index_id, platform_id))

                conn.commit()
                update_message = "Tool successfully updated."
                print(update_message)
            else:
                update_message = "Error: Tool not found for your company with that name."
                print(update_message)

        return render_template('dataUpdate.html', title='Gaitor Gate | Update', update_message=update_message)