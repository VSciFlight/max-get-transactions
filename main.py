"""Module responsible for running the program"""
import time
import func
import argum


def main():
    """
    The main function of the repository, showcase a high level view on the flow
    :return:
    """
    creds = argum.get_cli_arguments()

    driver = func.driver()
    time.sleep(2)
    func.max_login(driver, creds['email'], creds['password'])

    print(func.get_transactions(driver, creds['request'], creds))

    func.close_driver(driver)


if __name__ == '__main__':
    main()
