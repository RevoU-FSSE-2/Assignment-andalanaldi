import pytest
from unittest.mock import Mock, patch
from tweet.apis import post_tweet, flag_tweet

@pytest.fixture
def mock_authenticated_request():
    mock_request = Mock(headers={'Authorization': 'Token xyz'})
    mock_decode_jwt = Mock(return_value={'user_id': 'mock_user_id'})
    with patch('tweet.apis.decode_jwt', mock_decode_jwt):
        yield mock_request

def test_post_tweet(mock_authenticated_request):
    mock_authenticated_request.get_json.return_value = {"tweet": "This is a test tweet."}
    
    with patch('tweet.apis.User') as mock_user, patch('tweet.apis.Tweet') as mock_tweet, patch('tweet.apis.db.session.commit') as mock_commit:
        mock_user.query.get.return_value = Mock()
        mock_tweet.query.filter_by.return_value = Mock(count=0)

        # Assertions based on expected behavior
        response = post_tweet(mock_authenticated_request)
        assert 'id' in response  # Ensure 'id' is present in the response
        assert 'published_at' in response  # Ensure 'published_at' is present in the response
        assert 'tweet' in response  # Ensure 'tweet' is present in the response


def test_flag_tweet(mock_authenticated_request):
    mock_authenticated_request.get_json.return_value = {"tweet_id": 1, "is_spam": True}

    with patch('tweet.apis.User') as mock_user, patch('tweet.apis.Tweet') as mock_tweet, patch('tweet.apis.db.session.commit') as mock_commit:
        mock_user.query.get.return_value = Mock(role='MODERATOR')
        mock_tweet.query.get.return_value = Mock()

        # Assertions based on expected behavior
        response = flag_tweet(mock_authenticated_request)
        assert 'tweet_id' in response  # Ensure 'tweet_id' is present in the response
        assert 'is_spam' in response  # Ensure 'is_spam' is present in the response

