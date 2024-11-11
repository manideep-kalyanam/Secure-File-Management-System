import MySQLdb
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
    return g.db

def create_user(username, password, email, firstname, lastname):
    db = get_db()
    cursor = db.cursor()
    password_hash = generate_password_hash(password)
    query = """
    INSERT INTO User (username, password_hash, email, firstname, lastname) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (username, password_hash, email, firstname, lastname))
    db.commit()
    cursor.close()

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM User WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def insert_file(filename, s3_key, encrypted_aes_key, owner_id):
    db = get_db()
    cursor = db.cursor()
    query = """
        INSERT INTO File (filename, s3_key, encrypted_aes_key, owner_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (filename, s3_key, encrypted_aes_key, owner_id))
    db.commit()
    cursor.close()

def get_files_by_user(owner_id):
    db = get_db()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM File WHERE owner_id = %s"
    cursor.execute(query, (owner_id,))
    files = cursor.fetchall()
    cursor.close()
    return files

def share_file(file_id, recipient_id, encrypted_aes_key):
    db = get_db()
    cursor = db.cursor()
    query = """
        INSERT INTO SharedFile (file_id, recipient_id, encrypted_aes_key)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (file_id, recipient_id, encrypted_aes_key))
    db.commit()
    cursor.close()

def get_shared_files(recipient_id):
    db = get_db()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT File.filename, SharedFile.encrypted_aes_key
        FROM SharedFile
        JOIN File ON SharedFile.file_id = File.id
        WHERE SharedFile.recipient_id = %s
    """
    cursor.execute(query, (recipient_id,))
    shared_files = cursor.fetchall()
    cursor.close()
    return shared_files

# Add other functions wherever required
