import pytest
from unittest.mock import Mock, patch
from following.apis import follow_unfollow_user

@pytest.fixture
def mock_authenticated_request():
    mock_request = Mock(headers={'Authorization': 'Token xyz'})
    mock_decode_jwt = Mock(return_value={'user_id': 'mock_user_id'})
    with patch('following.apis.decode_jwt', mock_decode_jwt):
        yield mock_request

def test_follow_unfollow_user_follow(mock_authenticated_request):
    mock_authenticated_request.get_json.return_value = {"user_id": 123}
    
    with patch('following.apis.User') as mock_user, patch('following.apis.Following') as mock_following, patch('following.apis.db.session.commit') as mock_commit:
        mock_user.query.get.return_value = Mock()
        mock_user.query.filter_by.return_value = Mock()
        mock_following.query.filter_by.return_value = None

        response = follow_unfollow_user(mock_authenticated_request)
        assert 'following_status' in response  # Ensure 'following_status' is present in the response
        
        # Specific assertions based on the expected behavior of following someone
        assert response['following_status'] == 'follow'  # Assuming that if there's no existing follow, it returns 'follow'

def test_follow_unfollow_user_unfollow(mock_authenticated_request):
    mock_authenticated_request.get_json.return_value = {"user_id": 123}
    
    with patch('following.apis.User') as mock_user, patch('following.apis.Following') as mock_following, patch('following.apis.db.session.commit') as mock_commit:
        mock_user.query.get.return_value = Mock()
        mock_user.query.filter_by.return_value = Mock()
        mock_following.query.filter_by.return_value = Mock()

        response = follow_unfollow_user(mock_authenticated_request)
        assert 'following_status' in response  # Ensure 'following_status' is present in the response
        
        # Specific assertions based on the expected behavior of unfollowing someone
        assert response['following_status'] == 'unfollow'  # Assuming that if there's an existing follow, it returns 'unfollow'
