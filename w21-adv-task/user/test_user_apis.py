import pytest
from unittest.mock import Mock, patch
from user.apis import get_user_profile, get_user_feed, suspend_user

@pytest.fixture
def mock_authenticated_request():
    mock_request = Mock(headers={'Authorization': 'Token xyz'})
    mock_decode_jwt = Mock(return_value={'user_id': 'mock_user_id'})
    with patch('user.apis.decode_jwt', mock_decode_jwt):
        yield mock_request

def test_get_user_profile(mock_authenticated_request):
    response = get_user_profile(mock_authenticated_request)
    assert response['user_id'] == 'expected_user_id'
    # Add more assertions based on expected behavior
    assert 'username' in response
    assert 'bio' in response
    assert 'following' in response
    assert 'followers' in response
    assert 'tweets' in response

def test_get_user_feed(mock_authenticated_request):
    response = get_user_feed(mock_authenticated_request)
    # Add assertions for the response based on the expected behavior
    assert 'tweets' in response

def test_suspend_user():
    # To test suspend_user, you'll need to mimic the behavior of the 'decode_jwt' function and simulate the behavior of a moderator role.

    # Mocking request headers
    mock_request = Mock(headers={'Authorization': 'Token xyz'})
    mock_decode_jwt = Mock(return_value={'role': 'MODERATOR'})
    with patch('user.apis.decode_jwt', mock_decode_jwt):
        response = suspend_user(mock_request)
        # Add assertions for the response based on the expected behavior
        assert response["user_id"] == 'mock_user_id'
        assert response["is_suspended"] == 'expected_is_suspended'
