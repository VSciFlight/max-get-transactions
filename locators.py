"""Module responsible for storing locators within Max.co.il"""

max_loc: dict = {
    'personal_zone': ('xpath', '//*[contains(@class, "go-to-personal-area log-in-status")]'),
    'login_with_password': ('xpath', '//span[contains(text(), "כניסה עם סיסמה")]'),
    'login_with_id': ('xpath', '//*[@id="login-id-link"]'),
    'login_send_code': ('xpath', '//*[@id="send-code"]'),
    'login_button_login': ('xpath', '//*[@id="send-code" and @tabindex="3"]'),
    'input_id_number': ('xpath', '//input[@id="id-passport"]'),
    'input_username': ('xpath', '//input[@id="user-name"]'),
    'input_password': ('xpath', '//input[@id="password"]'),
    'login_error_msg': ('xpath', '//*[contains(@class, "error-msg bio-error")]'),
    'input_verify_code': ('xpath', '//input[@id="verify-code"]'),
    'input_verify_card': ('xpath', '//input[@id="card-num-bank"]'),
    'input_confirm_term': ('xpath', '//label[@for="confirmTerms"]'),
    'button_enter_personal_zone': ('xpath', '//button[@id="sen-me-code"]'),
    'transactions_list': ('xpath', '//*[@class="row body"]'),
    'transactions_date': ('xpath', '//*[@class="row body"]/div[1]'),
    'transactions_place': ('xpath', '//*[@class="row body"]/div[2]/div'),
    'transactions_card': ('xpath', '//*[@class="row body"]/div[4]'),
    'transactions_amount': ('xpath', '//*[@class="row body"]/div[6]/span'),
    'combo_dates': ('xpath', '//div[@class="combo dates"]'),
    'combo_dates_start': ('xpath', '//span[@class="date-title" and text()="תאריך התחלה"]'),
    'combo_dates_end': ('xpath', '//span[@class="date-title" and text()="תאריך סיום"]')
}
