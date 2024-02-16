# max-get-transactions

Repo for getting transactions in Max to a CSV file

![max-get-transactions](https://socialify.git.ci/VSciFlight/max-get-transactions/image?logo=https%3A%2F%2Fmedia.licdn.com%2Fdms%2Fimage%2FD4D03AQHxkHs-K9bSbA%2Fprofile-displayphoto-shrink_800_800%2F0%2F1673251636113%3Fe%3D1713398400%26v%3Dbeta%26t%3DD40rP28WlLGa-cyngSFNAQ2YsqCIMi6nvTfri7_MFGI&owner=1&theme=Auto)

## Background

Max is an israeli credit card company ("Leumi Card" in the past). <br>
Their website [max.co.il](www.max.co.il) is not much clear to me and I don't like going into it much. I only wanted to log inside and get my latest transactions from the website. I had an idea to create a tool that will do it for me! At first I thought about using an API to get transactions, seems legit and logical. However Max doesn't support this kind of methods of open-banking. So I had to adapt, improvise and act!

### The idea

I present to you another method which is scraping the data using Selenium! Because what doesn't work with mind, works with bigger mind.

## Requirements

* User (and probably credit card) in Max systems.
* Python

## How to use

to start using this tool all you have to do is follow this steps:

1. Clone this repository
2. Open the command line in the folder
3. Run the following command with the flags below

```
python main.py
```

## Flags

The whole program works through the command line and it needs the right flags.

### Required Flags
```
-e/--email the email address of the user
-p/--password the password of the user
-r/--request tells the request from the program
```

Email and password must be entered in order to log into the system (your credentials are not sent anywhere).

There are 4 requests you can type

* ytd - year to date, get all transactions from start of the year till today
* range - get all transaction within the range
* month - get all transaction within the month and year specified
* this_month - get all transaction within this month

For example a user wants the 'ytd' request he must enter:

```
python main -r ytd -e user@domain.com -p user_password
```

the month request requires month (-m) and year (-y) flags to be specified
for example if a user wants his transactions from January 2024 he must enter:

```
python main -r month -e user@domain.com -p user_password -m 1 -y 2024
```

> NOTE: Under month view Max shows transactions from today four years ago until today next year.

The range request asks a start date (-sd) and an end date (-ed).
For example if a user wants his transactions from January 7th 2023 until December 17th 2023 he must enter:

```
python main -r month -e user@domain.com -p user_password -sd 2023-01-07 -ed 2023-12-17
```

> NOTE: dates must be in the form of: YYYY-MM-DD. <br>
NOTE2: under range view Max shows transactions from today four years ago until today.

## Testing

in order to run the tests you must enter the details in the secret_file.py and then run the command from the main directory:

```
pytest tests
```

Otherwise the tests related to the user being logged in won't run properly.

## Built with

Technologies used in the project:

* Python
* Selenium
* Pandas
* Pytest
* Brain :brain:

## Bugs and Feature Requests

Some people asked me to tell about my progress in this project. You can see it on the [REFLECTION.md file](REFLECTION.md)

if you found any bugs or have an idea for features to add feel free to open a new [issue](https://github.com/VSciFlight/max-get-transactions/issues/new)
