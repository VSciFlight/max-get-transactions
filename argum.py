"""Module responsible for arguments parsing"""
import sys
import datetime

from argparse import ArgumentParser, Namespace, BooleanOptionalAction
from dateutil.relativedelta import relativedelta


# ARGUMENTS
parser = ArgumentParser()
parser._action_groups.pop()     # pylint: disable=protected-access

parser.add_argument_group('Required Arguments')
parser.add_argument('-r', '--request',
                    help='what transactions time frame do you want to extract?',
                    type=str,
                    choices={'this_month', 'ytd', 'month', 'range'},
                    required=True)

parser.add_argument_group('Completing Arguments According to Request')
parser.add_argument('-e', '--email',
                    help='write the email in which you enter to Max',
                    type=str)
parser.add_argument('-p', '--password',
                    help='write the password in which you enter to Max',
                    type=str)
parser.add_argument('-m', '--month',
                    help='write the month number you wish to get the report of '
                         '(0 means current month)',
                    choices={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'},
                    type=str)
parser.add_argument('-y', '--year',
                    help='write the year of the report you wish to get '
                         '(must be between next year and 4 years ago due Max restriction)',
                    type=str)
parser.add_argument('-sd', '--start_date',
                    help='write the date you wish to start '
                         'the report in YYYY-MM-DD format. example: 2024-03-31',
                    type=str)
parser.add_argument('-ed', '--end_date',
                    help='write the date you wish to end '
                         'the report in YYYY-MM-DD format. example: 2024-03-31',
                    type=str)
parser.add_argument('-nh', '--nohead',
                    help='use this flag in order to run in headless mode',
                    type=bool,
                    action=BooleanOptionalAction)

args: Namespace = parser.parse_args()


def args_check_creds() -> None:
    """
    check credentials were entered
    :return:
    """
    if args.email and args.password:
        print(f'your request is: {args.request}')
        print(f'this is your email: {args.email}')
        print(f'this is your password: {args.password}')

    else:
        sys.exit('No credentials were given')


def get_cli_arguments() -> dict:
    """Returns the CLI arguments as dictionary to main"""
    args_check_creds()
    month: str = month_converter(args.month)

    if args.request == 'range':
        range_date_validation(args.start_date, args.end_date)

    elif args.request == 'month':
        year_validation(args.year)
        month_validation(args.year, args.month)

    argx: dict = {"request": args.request, "email": args.email,
                  "password": args.password, "month": month, "year": args.year,
                  "start_date": args.start_date, "end_date": args.end_date,
                  "headless_mode": args.nohead}

    return argx


def month_converter(month: str) -> str:
    """process the month converting it to string instead of a number"""

    if month == '0':
        return 'this_month'

    if month is None:
        return ''

    if len(month) == 1:
        return '0' + month

    return month


def year_validation(year: str | None) -> None:
    """Validates year format"""
    if year is None:
        raise TypeError('year was not entered, please enter year and try again')

    if not len(year) == 4:
        raise ValueError('year must be 4 character long')

    if not year.isdigit():
        raise ValueError('year must contain only digits')


def range_date_validation(start_date: str, end_date: str) -> None:
    """process the start date and end date validation"""

    # FORMAT VALIDATION
    try:
        sd: datetime.date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        ed: datetime.date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    except ValueError:
        sys.exit('date format needs to look like this: "YYYY-MM-DD". example: 2024-03-31 \n'
                 f'you entered: start date: {start_date}. end date: {end_date}')
    except TypeError:
        sys.exit('start date (-sd) or end date (-ed) were not entered.\n'
                 f'you entered: start date: {start_date}. end date: {end_date}')

    # DATE RANGE VALIDATION
    try:
        if sd > datetime.date.today():
            raise ValueError('Start date cannot be later than today')
        if ed > datetime.date.today():
            raise ValueError('End date cannot be later than today')
        if sd > ed:
            raise ValueError('Start date cannot be later than end date')
        if sd < datetime.date.today() - relativedelta(years=4):
            raise ValueError('Max limits the range for transactions from the last four years')

    except ValueError as e:
        sys.exit(f' {e} \ndate value is invalid, '
                 f'date value needs to be from this month fours years ago until today \n'
                 f'you entered: start date: {start_date}. end date: {end_date}')


def month_validation(year: str, month: str) -> None:
    """process the month validation"""

    today_date: datetime.date = datetime.date.today()
    # Max saves transaction data from four years ago till next year under month view.
    try:
        if int(year) < today_date.year - 4 or int(year) > today_date.year + 1:
            raise ValueError(f'Year must be between four years ago ({today_date.year - 4})'
                             f' and next year ({today_date.year + 1}).'
                             f'You entered: {year}')

        if int(year) == today_date.year + 1 and int(month) > today_date.month:
            raise ValueError(f'Next year month cannot be greater than this month.'
                             f'You entered {year} and {month}')

        if int(year) == today_date.year - 4 and today_date.month > int(month):
            raise ValueError(f'Four years ago month cannot be smaller than this month.'
                             f'You entered {year} and {month}')

    except ValueError as e:
        sys.exit(f'{e}. \nPlease enter values in the correct time frame')
