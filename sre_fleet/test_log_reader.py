import unittest
from unittest.mock import patch, MagicMock
import json
import urllib.error

# Add the current directory to path if needed, but since we run from workspace root it should be fine if we use full module path or relative import.
# Let's use relative import or just assume it's in the same directory.
from sre_fleet.log_reader import read_logs, DEFAULT_URL

class TestLogReader(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_read_logs_success(self, mock_urlopen):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"message": "test log"}]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = read_logs()

        self.assertEqual(result, [{"message": "test log"}])
        mock_urlopen.assert_called_once()

    @patch('urllib.request.urlopen')
    def test_read_logs_http_error(self, mock_urlopen):
        # Setup mock to raise HTTPError
        mock_urlopen.side_effect = urllib.error.HTTPError(
            DEFAULT_URL, 403, 'Forbidden', None, None
        )

        result = read_logs()

        self.assertTrue(result.startswith("HTTP Error: 403"))

    @patch('urllib.request.urlopen')
    def test_read_logs_url_error(self, mock_urlopen):
        # Setup mock to raise URLError
        mock_urlopen.side_effect = urllib.error.URLError('reason')

        result = read_logs()

        self.assertTrue(result.startswith("URL Error: reason"))

    @patch('urllib.request.urlopen')
    def test_read_logs_invalid_json(self, mock_urlopen):
        # Setup mock response with invalid JSON
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'invalid json'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = read_logs()

        self.assertTrue(result.startswith("Error: Failed to decode JSON"))

if __name__ == '__main__':
    unittest.main()
