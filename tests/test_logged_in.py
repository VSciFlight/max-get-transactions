"""
Module aims to test functionality when user is logged in
"""
import glob
import os
import datetime
import calendar
import random
import subprocess
import csv
import pytest
from tests import secret_file # pylint: disable=no-name-in-module


class TestUserLoggedIn:
    """
    Test class that tests actions are being made properly
    Login process is being done in every test case here.
    All test are running in headless mode in order to save time and resources
    """

    today = datetime.date.today()
    this_month = today.month
    this_year = today.year

    next_month = today + datetime.timedelta(days=30)
    last_month = today - datetime.timedelta(days=30)

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
                                stdout=subprocess.PIPE,
                                text=True,
                                shell=True,
                                check=False)
        return result

    @staticmethod
    def get_csv_files() -> list:
        """
        a function to list all the csv files within the directory
        :return:
        """
        os.chdir(os.getcwd())
        file_list = glob.glob("*.csv")
        return file_list

    def create_range_random_valid_dates(self):
        """
        function to output a valid start date and a valid end date
        the dates must be within the timeframe
        :return:
        """
        year = random.randint(self.four_years_ago_today, self.this_year)
        if year == self.four_years_ago_today:
            month = random.randint(self.this_month, 12)
            days_in_month = calendar.monthrange(year, month)[1]
            day = random.randint(self.today.day, days_in_month)

        elif year == self.this_year:
            month = random.randint(1, self.this_month)
            if month == self.this_month:
                day = random.randint(1, self.today.day)

            else:
                days_in_month = calendar.monthrange(year, month)[1]
                day = random.randint(1, days_in_month)

        else:
            month = random.randint(1, 12)
            days_in_month = calendar.monthrange(year, month)[1]
            day = random.randint(1, days_in_month)

        start_date = datetime.date(year, month, day)
        delta_date = self.today - start_date
        end_date = start_date + datetime.timedelta(days=random.randint(1, delta_date.days))

        return start_date, end_date

    @staticmethod
    def get_range_within_file(csv_file: str) -> tuple[datetime.date, datetime.date]:
        """
        Function takes a csv file path in and returns the earliest and latest date within the file
        :param self:
        :param csv_file: path to the csv file
        :return:
        """
        file = open(csv_file, 'r', encoding='utf-8') # pylint: disable=consider-using-with
        csv_dict = csv.DictReader(file)
        file.close()

        dates_col = []

        for col in csv_dict:
            if not col['dates'] == '':
                dates_col.append(col['dates'])

        # csv is already sorted by dates
        min_date = datetime.datetime.strptime(str(dates_col[-1]), '%d/%m/%y')
        max_date = datetime.datetime.strptime(str(dates_col[0]), '%d/%m/%y')

        return min_date.date(), max_date.date()

    @pytest.fixture()
    def login_info(self):
        """
        a fixture assure successful login and cleaning the downloaded files at the end of the tests
        :return:
        """
        email = secret_file.account_info.get('email')
        password = secret_file.account_info.get('password')
        yield email, password

        # TEARDOWN
        csv_files_in_dir = self.get_csv_files()
        if len(csv_files_in_dir) > 0:
            for item in csv_files_in_dir:
                os.remove(item)

    @pytest.mark.ytd
    def test_ytd_process(self, login_info):
        """
        case where user asks for year-to-date transactions
        -r ytd is a request
        :return:
        """
        command = ['python', './main.py', '-r', 'ytd',
                   '-e', login_info[0], '-p', login_info[1]]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "ytd_transaction" in csv_files_in_dir[0]

    @pytest.mark.this_month
    def test_this_month_process(self, login_info):
        """
        case where user asks for this month

        :return:
        """
        command = ['python', './main.py', '-r', 'this_month',
                   '-e', login_info[0], '-p', login_info[1]]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "this_month" in csv_files_in_dir[0]

    @pytest.mark.month
    def test_month_any_month_this_year(self, login_info):
        """
        case where user asks for a month this year

        :return:
        """
        random_month = random.randint(1, 12)
        command = ['python', './main.py', '-r', 'month',
                   '-e', login_info[0], '-p', login_info[1],
                   '-m', str(random_month), '-y', str(self.this_year)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "month" in csv_files_in_dir[0]

    @pytest.mark.month
    def test_month_this_month_next_year(self, login_info):
        """
        case user asks for this month next year
        max case
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', login_info[0], '-p', login_info[1],
                   '-m', str(self.this_month), '-y', str(self.next_year)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "month" in csv_files_in_dir[0]

    @pytest.mark.month
    def test_month_this_month_four_years_ago(self, login_info):
        """
        case where user asks for transaction from four years ago
        min case
        :return:
        """
        command = ['python', './main.py', '-r', 'month',
                   '-e', login_info[0], '-p', login_info[1],
                   '-m', str(self.this_month), '-y', str(self.four_years_ago_today)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "month" in csv_files_in_dir[0]

    @pytest.mark.month
    def test_month_any_timeframe_between_this_month_next_year_and_four_years_ago(self, login_info):
        """
        case where user asks wants any month from four years ago to next year

        :return:
        """
        year = random.randint(self.four_years_ago_today, self.next_year)

        if year == self.four_years_ago_today:
            month = random.randint(self.this_month, 12)
        elif year == self.next_year:
            month = random.randint(1, self.this_month)
        else:
            month = random.randint(1, 12)

        command = ['python', './main.py', '-r', 'month',
                   '-e', login_info[0], '-p', login_info[1],
                   '-m', str(month), '-y', str(year)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "month" in csv_files_in_dir[0]

    @pytest.mark.range
    def test_range_max_limits(self, login_info):
        """
        case where user asks for all transactions from possible time frame
        covers all possible and valid dates and min-max dates
        :return:
        """
        start_date = datetime.date(self.four_years_ago_today, self.this_month, self.today.day)
        end_date = self.today
        command = ['python', './main.py', '-r', 'range',
                   '-e', login_info[0], '-p', login_info[1],
                   '-sd', str(start_date), '-ed', str(end_date)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "range" in csv_files_in_dir[0]

        min_date, max_date = self.get_range_within_file(csv_files_in_dir[0])

        assert min_date >= start_date
        assert max_date <= end_date

    @pytest.mark.range
    def test_range_random_range_within_timeframe(self, login_info):
        """
        case where user asks for any date within the timeframe
        note: the range view allows the time frame of today four years ago till today (this year)
        :return:
        """
        start_date, end_date = self.create_range_random_valid_dates()
        command = ['python', './main.py', '-r', 'range',
                   '-e', login_info[0], '-p', login_info[1],
                   '-sd', str(start_date), '-ed', str(end_date)]
        self.run_subprocess(command)

        csv_files_in_dir = self.get_csv_files()
        assert "range" in csv_files_in_dir[0]

        min_date, max_date = self.get_range_within_file(csv_files_in_dir[0])

        assert min_date >= start_date
        assert max_date <= end_date
