from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import get_files_by_user, get_shared_files
# from utils.encryption import encrypt_file_aes, decrypt_file_aes
# from utils.s3_utils import upload_file_to_s3, download_file_from_s3, delete_file_from_s3

file_bp = Blueprint('file', __name__)

# Dashboard route
@file_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Fetch user's files and shared files
    user_files = get_files_by_user(user_id)
    shared_files = get_shared_files(user_id)
    
    return render_template('dashboard.html', user_files=user_files, shared_files=shared_files)

# Upload a file route
@file_bp.route('/upload', methods=['POST'])
def upload_file():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    file = request.files['file']
    if file:
        # Encrypt the file using AES
        encrypted_file = encrypt_file_aes(file)
        
        # Upload the encrypted file to S3
        s3_url = upload_file_to_s3(encrypted_file)
        
        # Save file metadata to DB
        save_file_metadata(user_id, file.filename, s3_url)
        
        flash('File uploaded successfully!')
        return redirect(url_for('file.dashboard'))
    
    flash('No file selected.')
    return redirect(url_for('file.dashboard'))

# View and download a file route
@file_bp.route('/file/<int:file_id>', methods=['GET'])
def view_file(file_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    file_data = get_file_metadata(file_id, user_id)
    if not file_data:
        flash('File not found.')
        return redirect(url_for('file.dashboard'))
    
    decrypted_file = decrypt_file_aes(file_data['s3_url'])
    
    return render_template('view_file.html', file=decrypted_file)

# Delete a file route
# @file_bp.route('/delete/<int:file_id>', methods=['POST'])
# def delete_file(file_id):
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('auth.login'))
    
#     file_data = get_file_metadata(file_id, user_id)
#     if not file_data:
#         flash('File not found.')
#         return redirect(url_for('file.dashboard'))
    
#     # Delete from S3 and database
#     delete_file_from_s3(file_data['s3_url'])
#     delete_file_from_db(file_id)
    
#     flash('File deleted successfully!')
#     return redirect(url_for('file.dashboard'))
