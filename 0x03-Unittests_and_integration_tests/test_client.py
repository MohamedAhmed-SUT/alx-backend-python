from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
import unittest


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    # ... previous tests (test_org, test_public_repos_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names."""
        # Payload returned from get_json
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        # Value returned from _public_repos_url property
        test_url = "https://api.github.com/orgs/google/repos"

        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Verify result matches repo names
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Check both mocks were called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)
