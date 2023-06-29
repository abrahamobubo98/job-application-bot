import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()


def load_page():
    driver.get("REQUEST_LINK")


load_page()  # Loads the webpage
header_buttons = driver.find_elements(by=By.CSS_SELECTOR, value="header div a")
header_buttons[1].click()  # Clicks the sign-in button

# Signs in to LinkedIn
username = driver.find_element(by=By.CSS_SELECTOR, value="#username")
password = driver.find_element(by=By.CSS_SELECTOR, value="#password")
sign_in_button = driver.find_element(by=By.CSS_SELECTOR, value=".login__form_action_container")

username.send_keys("YOUR_EMAIL")
password.send_keys("YOUR_PASSWORD")
sign_in_button.click()

time.sleep(5)
jobs = driver.find_elements(by=By.CSS_SELECTOR, value=".ember-view a")


def apply():
    try:
        easy_apply_button = driver.find_element(by=By.CSS_SELECTOR, value=".jobs-apply-button--top-card button")
        easy_apply_button.click()
    except NoSuchElementException:
        print("Easy Apply button not found")
        application_status = driver.find_element(by=By.CSS_SELECTOR, value=".artdeco-inline-feedback")
        print(application_status.text)
        return "pass"
    except:
        return "pass"


def show_empty_fields(text_fields, menus):
    print("Empty Fields to be filled:")
    for text_field in text_fields:
        print(text_field.text)

    for menu in menus:
        print(menu.text)

    print(".............")


def fill_menu_options(value):
    unfiletered_options = driver.find_elements(by=By.CSS_SELECTOR,
                                               value=".jobs-easy-apply-form-section__grouping div select option")


def fill_text_fields(field, index, list_):
    question = list_[index]
    print("Text field question: ", question)

    if "experience" in question:
        field.send_keys("5")
        print(question, "5")
    elif "salary" in question:
        field.send_keys("110000")
        print(question, "110000")


def select_radio_buttons(questions):
    print("Radio buttons:", questions)
    radio_buttons = driver.find_elements(by=By.CSS_SELECTOR,
                                         value=".jobs-easy-apply-form-section__grouping div fieldset label")
    t = [r.text for r in radio_buttons]

    q_index = 0

    for q in questions:
        yes = q_index * 2
        no = q_index * 2 + 1
        if "drug test" in q:
            print("Are you willing to take a drug test, in accordance with local law? Yes")
            radio_buttons[yes].click()
        elif "legally authorised to work" in q:
            print("Work Authorization")
            radio_buttons[yes].click()
        elif "Bachelor's Degree?" in q:
            print("Have you completed the following level of education: Bachelor's Degree? Yes")
            radio_buttons[yes].click()
        elif "onsite" in q:
            print("Are you comfortable working in an onsite setting? No")
            radio_buttons[no].click()
        elif "remote" in q:
            print("Are you comfortable working in a remote setting?Yes")
            radio_buttons[yes].click()
        elif "hybrid" in q:
            print("Are you comfortable working in a hybrid setting? No")
            radio_buttons[no].click()
        elif "driver's license" in q:
            print("Do you have a valid driver's license? Yes")
            radio_buttons[yes].click()
        elif "background check" in q:
            print("Are you willing to undergo a background check, in accordance with local law/regulations? Yes")
            radio_buttons[yes].click()
        elif "require sponsorship for employment" in q:
            print(
                "Will you now, or in the future, require sponsorship for employment visa status (e.g. H-1B visa status)?")
            radio_buttons[no].click()
        elif "comfortable commuting" in q:
            print("Are you comfortable commuting to this job's location?")
            radio_buttons[no].click()

        q_index += 1
    print("Radio buttons selected")
    return len(questions)


def one_click_apply():
    # This if block applies if the application is just one page
    one_page_apply = driver.find_element(by=By.CSS_SELECTOR, value="footer button")
    if one_page_apply.text == "Submit application":
        one_page_apply.click()
        return


def check_form():
    title = driver.find_element(by=By.CSS_SELECTOR, value="h3").text
    time.sleep(1)
    entered_fields = 0

    all_form_field_objects = driver.find_elements(by=By.CSS_SELECTOR,
                                                  value=".jobs-easy-apply-form-section__grouping div label")
    all_form_field_objects_ii = driver.find_elements(by=By.CSS_SELECTOR,
                                                  value=".jobs-easy-apply-form-section__grouping div")
    text_field_objects = driver.find_elements(by=By.CSS_SELECTOR,
                                              value=".jobs-easy-apply-form-section__grouping div div div input")
    menu_objects = driver.find_elements(by=By.CSS_SELECTOR, value=".jobs-easy-apply-form-section__grouping div select")
    radio_button_objects = driver.find_elements(by=By.CSS_SELECTOR,
                                                value=".jobs-easy-apply-form-section__grouping div fieldset")

    all_form_fields = [field.text for field in all_form_field_objects]
    text_fields = [input_.text for input_ in text_field_objects]
    radio_button_questions = [radio.text for radio in radio_button_objects]
    menus = [menu.text for menu in all_form_field_objects_ii if "Select an option" in menu.text]

    all_form_fields = [field for field in all_form_fields if field not in ('Yes', 'No')]
    all_form_field_objects = [field for field in all_form_field_objects if field.text not in ('Yes', 'No')]

    text_questions = [question.text for question in all_form_field_objects if
                      question.text not in radio_button_questions and question.text not in menus]

    print("Text questions: ", text_questions)
    print("Number of text fields: ", len(text_fields))
    print("Menus: ", menus)

    for radio in radio_button_questions:
        all_form_fields.append(radio)

    for radio in radio_button_objects:
        all_form_field_objects.append(radio)

    radio_num = select_radio_buttons(radio_button_questions)
    entered_fields += radio_num

    print("Form fields after checking for radio buttons:", all_form_fields)
    text_field_index = 0
    for value in text_field_objects:
        print(f"Text field value: {value.get_attribute('value')}")
        if value.get_attribute('value') != '':
            entered_fields += 1
        else:
            fill_text_fields(value, text_field_index, text_questions)
            entered_fields += 1
        text_field_index += 1

    menu_index = 0
    for value in menu_objects:
        print(f"Menu value: {value.get_attribute('value')}")
        if value.get_attribute('value') != 'Select an option':
            entered_fields += 1
        else:
            fill_menu_options(value)
            print(value.text)
    print("Entered fields: ", entered_fields)
    print("Total fields: ", len(all_form_fields))

    if len(all_form_fields) > 0:
        if entered_fields == len(all_form_fields):
            print("All fields complete")

            if driver.find_element(by=By.CSS_SELECTOR, value="h3").text == "Contact info":
                next_button_1 = driver.find_element(by=By.CSS_SELECTOR, value="form button")
                next_button_1.click()
                print("Next button clicked")
            else:
                next_button_2 = driver.find_elements(by=By.CSS_SELECTOR, value="footer button")
                next_button_2[1].click()
                print("Next button clicked")
            return
        else:
            show_empty_fields(text_field_objects, menu_objects)

    elif title == "Resume":
        next_button_2 = driver.find_elements(by=By.CSS_SELECTOR, value="footer button")
        next_button_2[1].click()
        print("Next button clicked")
    elif title == "Review your application":
        return
    else:
        print("Entered fields:", entered_fields)
        print("Total fields: ", len(all_form_fields))
        print("Form not completed")
        sys.exit(1)


def submit_app():
    time.sleep(5)
    unfollow_company = driver.find_element(by=By.CSS_SELECTOR, value=".job-details-easy-apply-footer__section label")
    unfollow_company.click()
    submit_application = driver.find_elements(by=By.CSS_SELECTOR, value="footer button")
    submit_application[1].click()
    time.sleep(1)
    close = driver.find_element(by=By.CSS_SELECTOR, value="button")
    close.click()


for job in jobs:
    print("Job title: ", job.text)

    job.click()
    job.click()
    time.sleep(2)
    a = apply()
    if a == "pass":
        continue
    time.sleep(1)
    try:
        form_completeness = driver.find_element(by=By.CSS_SELECTOR, value=".artdeco-completeness-meter-linear div")
        print(f"Form Completeness: {form_completeness.text}")
    except NoSuchElementException:
        one_click_apply()

    header = driver.find_element(by=By.CSS_SELECTOR, value="h3").text
    print(header)
    while header != 'Review your application':
        check_form()
        header = driver.find_element(by=By.CSS_SELECTOR, value="h3").text
        print(header)
    submit_app()
