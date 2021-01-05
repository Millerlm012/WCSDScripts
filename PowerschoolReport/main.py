import time
from datetime import datetime, timedelta
from config import *
from selenium import webdriver
import pandas as pd
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

'''
!!note for first time use!!
for manual USER running python script -> chromedriver needs to be in PATH: for mac terminal -> mv chromedriver /usr/local/bin
for automatic CRONTAB running python script -> must specify full chromedriver path when initializing webdriver
selenium web driver documentation: https://selenium-python.readthedocs.io/
'''


def date_variables():

    # today's date
    current_date = datetime.today()
    # today's date + 7 day
    today_plus_seven = datetime.today() + timedelta(days=7)
    # today's date + 14 day
    today_plus_fourteen = datetime.today() + timedelta(days=14)

    # format the date to dd/mm/yyyy
    current_date_format = current_date.strftime('%m' + '/' + '%d' + '/' + '%Y')
    today_plus_seven_format = today_plus_seven.strftime('%m' + '/' + '%d' + '/' + '%Y')
    today_plus_fourteen_format = today_plus_fourteen.strftime('%m' + '/' + '%d' + '/' + '%Y')

    # ps 7 day search query
    ps_7day_search_query = '/schoolid<1000;enroll_status<=0;entrydate<' + today_plus_seven_format
    # ps 14 day search query
    ps_14day_search_query = '/schoolid<1000;enroll_status<=0;entrydate<' + today_plus_fourteen_format

    return ps_7day_search_query, ps_14day_search_query, current_date_format


def powerschool():

    # retrieving variables from other functions
    ps_7day_search_query, ps_14day_search_query, current_date_format = date_variables()

    # initializes the chrome webdriver
    powerschool_admin_link = 'POWERSCHOOL LOGIN PORTAL'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.create_options()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

    # goes to powerschool admin link
    driver.get(powerschool_admin_link)
    time.sleep(3)

    # clicks on username query: logs in
    username_query = driver.find_element_by_id('fieldUsername')
    for i in range(len(login_username)):
        username_query.send_keys(login_username[i])
        time.sleep(.5)
        i += 1
    time.sleep(4)

    # clicks on password query: logs in
    password_query = driver.find_element_by_id('fieldPassword')
    for i in range(len(login_password)):
        password_query.send_keys(login_password[i])
        time.sleep(.5)
    time.sleep(4)

    # clicks on sign in  button
    sign_in_button = driver.find_element_by_id('btnEnter')
    sign_in_button.click()
    time.sleep(4)

    # clicks on DO button
    do_button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/span[1]/span[1]/a[19]')
    do_button.click()
    time.sleep(5)

    # finds search query bar and inputs search query
    search_query = driver.find_element_by_id('studentSearchInput')
    search_query.send_keys(ps_14day_search_query)
    time.sleep(5)

    # finds search button and clicks it
    search_button = driver.find_element_by_id('searchButton')
    search_button.click()
    time.sleep(5)

    # finds special functions button and clicks it
    special_functions = driver.find_element_by_id('navSpecialFunctions')
    special_functions.click()
    time.sleep(5)

    # finds importing and exporting option and clicks it
    import_export_option = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/table/tbody/tr[8]/td[1]/a')
    import_export_option.click()
    time.sleep(5)

    # finds export using template option and clicks it
    export_using_template_option = driver.find_element_by_xpath('/html/body/div[1]/div[5]/div[3]/table/tbody/tr[10]/td[1]/a')
    export_using_template_option.click()
    time.sleep(5)

    # finds export box and clicks it
    export_box = driver.find_element_by_xpath('/html/body/form/div[1]/div[5]/div[3]/table/tbody/tr[2]/td[2]/select')
    export_box.click()
    time.sleep(5)

    # finds student option and clicks it
    student_option = driver.find_element_by_xpath('/html/body/form/div[1]/div[5]/div[3]/table/tbody/tr[2]/td[2]/select/option[2]')
    student_option.click()
    time.sleep(5)

    # finds export template and clicks it
    export_template_box = driver.find_element_by_xpath('/html/body/form/div[1]/div[5]/div[3]/table/tbody/tr[3]/td[2]/select/option[1]')
    export_template_box.click()
    time.sleep(5)

    # finds 1:1 student option and clicks it
    one_to_one_student_option = driver.find_element_by_xpath('/html/body/form/div[1]/div[5]/div[3]/table/tbody/tr[3]/td[2]/select/option[8]')
    one_to_one_student_option.click()
    time.sleep(5)

    # chooses all student records circle and clicks it
    student_records_circle = driver.find_element_by_xpath('/html/body/form/div[1]/div[5]/div[3]/table/tbody/tr[4]/td[2]/p/input[2]')
    student_records_circle.click()
    time.sleep(5)

    # finds submit button and clicks it
    submit_button = driver.find_element_by_id('btnSubmit')
    submit_button.click()
    time.sleep(5)

    # renames the .text files and moves it to project directory
    os.rename(r'/Users/lmiller/Downloads/student.export.text', r'/Users/lmiller/PythonProjects/powerschoolReportScript/exportedData/' + current_date_format + '.student.export.text')

    # imports the .text file from the downloads directory and converts it to a .csv file in the projects directory then moves it to imported data folder
    student_data = pd.read_csv(r'/Users/lmiller/PythonProjects/powerschoolReportScript/exportedData' + current_date_format + 'student.export.text')
    student_data.to_csv(r'/Users/lmiller/PythonProjects/powerschoolReportScript/importedData/' + current_date_format + 'student.import.csv', index=None)


def convert_and_copy_downloaded_data():

    ps_7day_search_query, ps_14day_search_query, current_date_format = date_variables()

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('PowerschoolReportScript-aafe277a550b.json', scope)
    client = gspread.authorize(creds)

    gc = gspread.authorize(creds)

    # Read CSV file contents
    content = open('/Users/lmiller/PythonProjects/powerschoolReportScript/importedData/' + current_date_format + 'student.import.csv', 'r').read()

    # imports .csv data to gspreadsheet
    gc.import_csv('12Cyjzhsc1NKXmASTLdLXqN9QBc1QIRCb-dfK8vfY2Mc', content)


if __name__ == '__main__':
    powerschool()
