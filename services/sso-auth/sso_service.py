# File: services/sso-auth/sso_service.py
import os
import jwt
import datetime
import psycopg2
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

class SingleSignOnService:
    def __init__(self, db_config):
        self.app = Flask(__name__)
        self.app.secret_key = os.environ.get('AUTH_SECRET_KEY')
        self.db_connection = psycopg2.connect(**db_config)
        
        # SSO Endpoints
        self.app.route('/login', methods=['POST'])(self.login)
        self.app.route('/logout', methods=['POST'])(self.logout)
        self.app.route('/validate_token', methods=['GET'])(self.validate_token)

    def authenticate_user(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, role_id 
            FROM users 
            WHERE username = %s AND is_active = TRUE
        """, (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            return user
        return None

    def generate_token(self, user_id, username, role_id):
        return jwt.encode({
            'user_id': user_id,
            'username': username,
            'role_id': role_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, self.app.secret_key, algorithm='HS256')

    def get_user_permissions(self, role_id):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT resource, access_level 
            FROM permissions 
            WHERE role_id = %s
        """, (role_id,))
        return {perm[0]: perm[1] for perm in cursor.fetchall()}

    def login(self):
        credentials = request.json
        user = self.authenticate_user(
            credentials['username'], 
            credentials['password']
        )
        
        if user:
            token = self.generate_token(user[0], user[1], user[3])
            permissions = self.get_user_permissions(user[3])
            
            return jsonify({
                'token': token,
                'username': user[1],
                'permissions': permissions
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401

    def logout(self):
        # Token invalidation logic can be added here
        return jsonify({'message': 'Logged out successfully'}), 200

    def validate_token(self):
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(token, self.app.secret_key, algorithms=['HS256'])
            return jsonify({
                'valid': True,
                'user_id': payload['user_id'],
                'username': payload['username'],
                'role_id': payload['role_id']
            }), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'valid': False, 'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'valid': False, 'error': 'Invalid token'}), 401

# Configuration initialization
SSO_CONFIG = {
    'dbname': os.environ.get('QWC_DB_NAME'),
    'user': os.environ.get('QWC_DB_USER'),
    'password': os.environ.get('QWC_DB_PASSWORD'),
    'host': os.environ.get('QWC_DB_HOST')
}

sso_service = SingleSignOnService(SSO_CONFIG)
app = sso_service.app
