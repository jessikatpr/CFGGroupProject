import unittest
from unittest import TestCase
from unittest.mock import patch

from Project_CFG2 import savings_account, menu


class SavingsAccountTestCase(TestCase):

    @patch('builtins.input', side_effect=['a', '1000', '5'])
    @patch('builtins.print')
    def test_savings_account_instant_access(self, mock_print, mock_input):
        # Test Instant Access Savings calculation
        savings_account()
        mock_print.assert_called_with(
            "If you choose NatWest you'll earn £125.51 in interest after 5"
        )

    @patch('builtins.input', side_effect=['b', '2000', '2'])
    @patch('builtins.print')
    def test_savings_account_fixed_bonds_less_than_3_years(self, mock_print, mock_input):
        # Test Fixed Bonds calculation with less than 3 years
        savings_account()
        mock_print.assert_called_with(
            "If you choose NatWest you'll earn £162.88 in interest after 2"
        )

    @patch('builtins.input', side_effect=['b', '3000', '4'])
    @patch('builtins.print')
    def test_savings_account_fixed_bonds_more_than_3_years(self, mock_print, mock_input):
        # Test Fixed Bonds calculation with 3 or more years
        savings_account()
        mock_print.assert_called_with(
            "If you choose NatWest you'll earn £230.03 in interest after 4"
        )

    @patch('builtins.input', return_value='0')
    @patch('builtins.print')
    def test_menu_exit(self, mock_print, mock_input):
        # Test menu choice 0 (exit)
        menu()
        mock_print.assert_called_with("Goodbye!")

    @patch('builtins.input', side_effect=['3', '0'])
    @patch('builtins.print')
    def test_menu_invalid_choice(self, mock_print, mock_input):
        # Test menu with invalid choice
        menu()
        mock_print.assert_called_with("Invalid choice. Please enter 0, 1 or 2")


if __name__ == '__main__':
    unittest.main()
