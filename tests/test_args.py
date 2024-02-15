"""
Module providing tests for the arguments logic and behavior.
These tests do not require actual login
"""
import datetime
import subprocess
import pytest

# pylint: disable=too-many-public-methods
class TestArgumLogic:
    """
    Unittest class to test the arguments variables and their actions
    These tests checking its failing conditions, so out of scope parameters won't be processed
    """
    # TIME WISE
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    this_month = today.month
    next_month = today + datetime.timedelta(days=31)
    last_month = today - datetime.timedelta(days=31)
    this_year = today.year
    four_years_ago_today = this_year - 4
    next_year = this_year + 1

    @staticmethod
    def run_subprocess(command) -> subprocess.CompletedProcess:
        """
        subprocess to run the command line arguments
        :param command:
        :return:
        """
        result = subprocess.run(command,
                                stderr=subprocess.PIPE,
                                text=True,
                                shell=True,
                                check=False)
        return result

    # REQUEST ARGUMENT
    @pytest.mark.request
    def test_no_request(self):
        """
        tests when user doesn't supply a request argument
        :return:
        """
        command = ['python', './main.py']
        result = self.run_subprocess(command)

        assert 'error: the following arguments are required: -r/--request' in result.stderr

    @pytest.mark.request
    def test_unlisted_request(self):
        """
        case when user tries to run an unlisted request
        :return:
        """
        command = ['python', './main.py', '-r', 'stub']
        result = self.run_subprocess(command)

        assert "invalid choice: 'stub'" in result.stderr

    @pytest.mark.request
    def test_empty_request(self):
        """
        case when a user tries to run an empty request
        or any empty argument
        :return:
        """
        command = ['python', './main.py', '-r']
        result = self.run_subprocess(command)

        assert "error: argument -r/--request: expected one argument" in result.stderr

    @pytest.mark.request
    def test_multiple_request(self):
        """
        case when a user tries to run multiple requests
        :return:
        """
        command = ['python', './main.py', '-r', '\'month range\'']
        result = self.run_subprocess(command)

        assert "error: argument -r/--request: invalid choice" in result.stderr

    # CREDENTIALS
    @pytest.mark.credentials
    def test_no_credentials_given(self):
        """
        Tests when a user doesn't supply email or password
        :return:
        """
        command = ['python', './main.py', '-r', 'month']
        result = self.run_subprocess(command)

        assert 'No credentials were given\n' in result.stderr

    @pytest.mark.credentials
    def test_wrong_credentials(self):
        """
        Tests when a user doesn't supply correct email or password
        :return:
        """
        command = ['python', './main.py', '-r', 'ytd',
                   '-e', 'test@mdasd.com', '-p', '123456789']
        result = self.run_subprocess(command)

        assert 'Error with credentials at Max' in result.stderr

    # RANGE
    @pytest.mark.range
    def test_range_not_defined(self):
        """
        Testing a case where user wants a range but enters no start date or end date
        :return:
        """
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545']
        result = self.run_subprocess(command)

        assert 'start date (-sd) or end date (-ed) were not entered' in result.stderr

    @pytest.mark.range
    def test_range_dates_incorrect_format(self):
        """
        Testing a case where user requests a range but enters incorrect date format
        :return:
        """
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-sd', '31/7/2024', '-ed', '31072024']
        result = self.run_subprocess(command)

        assert 'date format needs' in result.stderr

    @pytest.mark.range
    def test_range_start_date_is_later_than_today(self):
        """
        Testing a case where user tries to enter a start date later than today
        :return:
        """
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-sd', str(self.tomorrow), '-ed', str(self.next_month)]
        result = self.run_subprocess(command)

        assert 'Start date cannot be later than today' in result.stderr

    @pytest.mark.range
    def test_range_end_date_is_later_than_today(self):
        """
        Testing a case where user tries to enter an end date later than today
        :return:
        """
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-sd', str(self.yesterday), '-ed', str(self.tomorrow)]
        result = self.run_subprocess(command)

        assert 'End date cannot be later than today' in result.stderr

    @pytest.mark.range
    def test_range_start_date_is_after_end_date(self):
        """
        Testing a case where user tries to enter a start date later than the end date
        :return:
        """
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-sd', str(self.today), '-ed', str(self.yesterday)]
        result = self.run_subprocess(command)

        assert 'Start date cannot be later than end date' in result.stderr

    @pytest.mark.range
    def test_range_start_date_is_before_four_years_ago(self):
        """
        case where user tries to enter a start date before four years ago.
        According to Max they keep transaction records from today four years ago
        until today under the range view
        :return:
        """
        four_years_ago_yesterday = datetime.date(self.four_years_ago_today,
                                                 self.this_month,
                                                 self.yesterday.day)
        command = ['python', './main.py', '-r', 'range',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-sd', str(four_years_ago_yesterday), '-ed', str(self.today)]
        result = self.run_subprocess(command)

        assert 'Max limits the range for transactions from the last four years' in result.stderr

    # MONTH
    # month argument (-m) must come with year argument (-y)
    @pytest.mark.month
    def test_month_empty_choice(self):
        """
        case where user tries to request a month without specifying which month
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '', '-y', str(self.this_year)]
        result = self.run_subprocess(command)

        assert 'invalid choice: ' in result.stderr

    @pytest.mark.month
    def test_month_unlisted_choice(self):
        """
        case where user tries to request a month without specifying which month
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '13', '-y', str(self.this_year)]
        result = self.run_subprocess(command)

        assert 'invalid choice: ' in result.stderr

    @pytest.mark.month
    def test_month_with_no_year_argument(self):
        """
        case where user tries to request a month without specifying which month
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '1']
        result = self.run_subprocess(command)

        assert 'year was not entered' in result.stderr

    @pytest.mark.month
    def test_month_year_empty(self):
        """
        case where user tries to request a month without specifying which month
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '1', '-y', '']
        result = self.run_subprocess(command)

        assert 'year must be 4 character long' in result.stderr

    @pytest.mark.month
    def test_month_year_is_later_than_next_year(self):
        """
        case where user tries to request a year that is later than next year
        :return:
        """
        in_two_years = str(self.next_year + 1)
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '1', '-y', in_two_years]
        result = self.run_subprocess(command)

        assert 'Year must be between four years ago' in result.stderr

    @pytest.mark.month
    def test_month_year_is_earlier_than_four_years_ago(self):
        """
        case where user tries to request a year that is earlier than four years ago
        :return:
        """
        five_years_ago = str(self.this_year - 5)
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', '1', '-y', five_years_ago]
        result = self.run_subprocess(command)

        assert 'Year must be between four years ago' in result.stderr

    @pytest.mark.month
    def test_month_next_year_month(self):
        """
        case where user tries to request next year month
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', str(self.next_month.month), '-y', str(self.next_year)]
        result = self.run_subprocess(command)

        assert 'Next year month cannot be greater than this month' in result.stderr

    @pytest.mark.month
    def test_month_last_month_four_years_ago(self):
        """
        case where user tries to request last month four years ago
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', 'test@example.com', '-p', '165121545',
                   '-m', str(self.last_month.month), '-y', str(self.four_years_ago_today)]
        result = self.run_subprocess(command)

        assert 'Four years ago month cannot be smaller than this month' in result.stderr
