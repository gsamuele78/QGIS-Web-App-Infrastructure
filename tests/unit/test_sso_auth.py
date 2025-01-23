# File: tests/unit/test_sso_auth.py
import pytest
from services.sso_auth.sso_service import SingleSignOnService

@pytest.fixture
def mock_db_config():
    return {
        'dbname': 'test_db',
        'user': 'test_user',
        'password': 'test_password',
        'host': 'localhost'
    }

class TestSSOAuthentication:
    def test_token_generation(self, mock_db_config):
        sso_service = SingleSignOnService(mock_db_config)
        token = sso_service.generate_token(1, 'testuser', 2)
        assert token is not None
        assert isinstance(token, str)

    def test_validate_token(self, mock_db_config):
        sso_service = SingleSignOnService(mock_db_config)
        token = sso_service.generate_token(1, 'testuser', 2)
        
        # Simulate token validation
        with pytest.raises(Exception):
            sso_service.validate_token(token + 'invalid')
