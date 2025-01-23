# File: services/qgis-desktop/sso_auth.py
import os
import requests
import json
import logging

class QGISDesktopSSO:
    def __init__(self, sso_url=None):
        self.sso_url = sso_url or os.environ.get('SSO_AUTH_URL', 'http://sso-auth:5000')
        self.token_file = '/home/qgis/.sso_token'
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def authenticate(self, username, password):
        """Authenticate user with SSO service"""
        try:
            response = requests.post(
                f"{self.sso_url}/login", 
                json={
                    'username': username, 
                    'password': password
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self._save_token(token_data)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False

    def validate_token(self):
        """Validate existing token"""
        if not os.path.exists(self.token_file):
            return False
        
        try:
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            
            response = requests.get(
                f"{self.sso_url}/validate_token",
                headers={'Authorization': token_data['token']}
            )
            
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Token validation failed: {e}")
            return False

    def _save_token(self, token_data):
        """Save authentication token"""
        with open(self.token_file, 'w') as f:
            json.dump(token_data, f)

    def get_user_permissions(self):
        """Retrieve user permissions"""
        try:
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            
            return token_data.get('permissions', {})
        except Exception as e:
            self.logger.error(f"Failed to retrieve permissions: {e}")
            return {}

def main():
    sso = QGISDesktopSSO()
    
    # Example usage
    username = os.environ.get('QGIS_USERNAME')
    password = os.environ.get('QGIS_PASSWORD')
    
    if username and password:
        if sso.authenticate(username, password):
            print("Authentication successful")
            permissions = sso.get_user_permissions()
            print(f"User Permissions: {permissions}")
        else:
            print("Authentication failed")

if __name__ == '__main__':
    main()
