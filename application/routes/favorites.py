from flask import Blueprint, render_template, request, redirect, session, current_app, url_for
from flask_login import login_required, current_user
import MySQLdb.cursors

RESULTS_PER_PAGE = 3

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/toggle_favorite', methods=['POST'])
@login_required
def toggle_favorite():
    """Add or remove a favorite"""
    with current_app.app_context():
        conn = current_app.config['MYSQL'].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        index_id = request.form.get('index_id')
        account_id = current_user.id
        # Check if this is already a favorite
        cursor.execute(
            "SELECT idFavorite FROM Favorite WHERE idAccount = %s AND idIndex = %s",
            (account_id, index_id)
        )
        existing_favorite = cursor.fetchone()
        
        if existing_favorite:
            # Remove favorite
            cursor.execute(
                "DELETE FROM Favorite WHERE idAccount = %s AND idIndex = %s",
                (account_id, index_id)
            )
            print(f"Removed favorite for User ID {account_id}, Index ID {index_id}")
        else:
            # Add favorite
            cursor.execute(
                "INSERT INTO Favorite (idAccount, idIndex) VALUES (%s, %s)",
                (account_id, index_id)
            )
            print(f"Added favorite for User ID {account_id}, Index ID {index_id}")
        
        conn.commit()
        cursor.close()
        
        # Redirect back to the previous page
        referrer = request.referrer or url_for('search.search')
        return redirect(referrer)


@favorites_bp.route('/saved', methods=['GET'])
@login_required
def view_saved():
    """View all saved favorites for the current user"""
    with current_app.app_context():
        conn = current_app.config['MYSQL'].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # First get the idUser from the Account table
        cursor.execute(
            "SELECT idUser, username, email FROM Account WHERE idAccount = %s",
            (current_user.id,)
        )
        user_result = cursor.fetchone()
        
        if not user_result:
            print(f"Could not find User ID for Account ID {current_user.id}")
            return render_template('saved.html', data=[], user={'username': 'User'}, title="Gaitor Gate | Favorites")
            
        user_id = user_result['idUser']
        username = user_result['username']
        email = user_result.get('email', '')
        account_id = current_user.id
        # Get all favorites with tool information
        cursor.execute("""
            SELECT 
                f.idFavorite, 
                si.idIndex,
                t.idTool,
                t.description,
                t.name,
                co.company_name AS company,
                t.url,
                t.thumbnail_url,
                t.published_date,
                t.pricing,
                t.version,
                c.name AS category
            FROM Favorite f
            JOIN SearchIndex si ON f.idIndex = si.idIndex
            JOIN Tools t ON si.idTool = t.idTool
            LEFT JOIN Category c ON si.idCategory = c.idCategory
            JOIN Company co ON t.company = co.idAccount
            WHERE f.idAccount = %s
            GROUP BY si.idIndex, t.idTool, t.description, t.name, t.company, t.url, t.thumbnail_url, t.published_date, t.pricing, t.version, c.name      
            ORDER BY f.idFavorite DESC
        """, (account_id,))
        
        favorites = cursor.fetchall()
        total_results = len(favorites)
        total_pages = (total_results + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

        page = request.args.get("page", 1, type=int)
        offset = (page - 1) * RESULTS_PER_PAGE
        data = favorites[offset : offset + RESULTS_PER_PAGE]
        cursor.close()
        
        title = f"Gaitor Gate | {username}'s Favorites"
        return render_template('saved.html', data=data, user={'username': username, 'email': email}, title=title, current_page=page, total_pages=total_pages)

@favorites_bp.route('/clear_favorites', methods=['POST'])
@login_required
def clear_favorites():
    """Clear all favorites for the current user"""
    conn = current_app.config['MYSQL'].connection
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "DELETE FROM Favorite WHERE idAccount = %s",
            (current_user.id,)
        )
        conn.commit()
        response = {"status": "success", "message": "Favorites cleared successfully"}
        return response, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        conn.rollback()
        response = {"status": "error", "message": str(e)}
        return response, 500, {'Content-Type': 'application/json'}
    finally:
        cursor.close()

# Helper function to check if an item is favorited
def is_favorited(index_id, account_id):
    """Check if an item is favorited by the user"""
    if not account_id:
        return False
        
    with current_app.app_context():
        conn = current_app.config['MYSQL'].connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        # First get the idUser from the Account table
        cursor.execute(
            "SELECT idUser FROM Account WHERE idAccount = %s",
            (account_id,)
        )
        user_result = cursor.fetchone()
        
        if not user_result:
            return False
            
        actual_user_id = user_result['idUser']
        
        cursor.execute(
            "SELECT 1 FROM Favorite WHERE idAccount = %s AND idIndex = %s",
            (account_id, index_id)
        )
        result = cursor.fetchone() is not None
        cursor.close()
        return result 