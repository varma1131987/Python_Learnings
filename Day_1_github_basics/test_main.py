"""Import unittest and unittest.mock: These are used for testing and mocking the print function.
Patch the print function: The @patch decorator replaces print with a mock object to capture its calls.
Assert the output: Verify that print was called with the expected string.
You can run the tests using the following command in the terminal"""

import unittest
from unittest.mock import patch
from main import main

class TestMainFunction(unittest.TestCase):
    @patch("builtins.print")
    def test_main_output(self, mock_print):
        # Call the main function
        main()
        # Assert that print was called with the expected output
        mock_print.assert_called_once_with("Hello from python-learnings!")

if __name__ == "__main__":
    unittest.main()

    

