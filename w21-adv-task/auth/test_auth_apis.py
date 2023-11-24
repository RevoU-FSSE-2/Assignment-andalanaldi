import pytest
from unittest.mock import Mock, patch
from auth.apis import register, login

@pytest.fixture
def mock_request():
    return Mock()

def test_register(mock_request):
    mock_request.get_json.return_value = {
        "username": "test_user",
        "password": "test_password",
        "bio": "test_bio",
        "role": "USER"
    }
    
    with patch('auth.apis.bcrypt') as mock_bcrypt:
        mock_bcrypt.generate_password_hash.return_value = 'hashed_password'

        response = register()
        assert response['user_id'] == 'expected_user_id'
        assert response['username'] == 'test_user'  # Check if username matches
        assert response['bio'] == 'test_bio'  # Check if bio matches
        assert response['role'] == 'USER'  # Check if role is set as USER        
        # Add more assertions based on expected behavior

def test_login(mock_request):
    mock_request.get_json.return_value = {
        "username": "test_user",
        "password": "test_password"
    }

    with patch('auth.apis.bcrypt') as mock_bcrypt:
        mock_user = Mock()
        mock_user.user_id = 'mock_user_id'
        mock_user.username = 'test_user'
        mock_user.bio = 'test_bio'
        mock_user.role = 'USER'
        mock_user.is_suspended = False
        mock_user.password = 'hashed_password'

        mock_request.side_effect = lambda: mock_user if 'Authorization' in mock_request.headers else None

        response = login()
        assert 'token' in response
        # Add more assertions based on expected behavior
