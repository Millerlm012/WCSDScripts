# creating a bash script on the checkout iMac to ssh into thescriptingmachine and run this python script to handle the new students

from selenium import webdriver
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
from config import *
import gspread
import os
import time


# fetches the data for the new students
def gspreadData():

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('PowerschoolReportScript-aafe277a550b.json', scope)
    client = gspread.authorize(creds)

    gc = gspread.authorize(creds)

    # fetching the student information from 'New Student Labels Prep' tab
    # retrieving spreadsheet by url
    itprintinglabels_sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/17c88xz1_kzgLt_QuNPGq7i2xrIYcPgVczHGDp1nUpQo/edit#gid=1836712917')
    # retrieving proper worksheet by name
    newstudentlabelsprep_worksheet = itprintinglabels_sheet.worksheet('New Student Labels Prep')
    # fetching all student data from column 'A' and 'B' -> this will retrieve the student's full name and id number
    columna_values = newstudentlabelsprep_worksheet.col_values(1)
    columnb_values = newstudentlabelsprep_worksheet.col_values(2)

    print('all student names - ' + str(columna_values))
    print('all student id numbers - ' + str(columnb_values))

    print('-------------------------------------------------------------------')


    createHappyfoxNote(columna_values, columnb_values)


def createHappyfoxNote(columna_values, columnb_values):

    # initiate chromedriver
    happyfox_link = 'HAPPYFOXURL'
    enter = u'\ue007'
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
    driver.create_options()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    # go to happyfox url
    driver.get(happyfox_link)

    # log into happyfox | username
    username_query = driver.find_element_by_id('id_username')
    for i in range(len(login_username)):
        username_query.send_keys(login_username[i])
        time.sleep(.5)
        i += 1
    time.sleep(4)

    # log into happyfox | password
    password_query = driver.find_element_by_id('id_password')
    for i in range(len(login_password)):
        password_query.send_keys(login_password[i])
        time.sleep(.5)
        i += 1
    password_query.send_keys(enter)
    time.sleep(8)

    # creating variable for range to be 1 less than the length of the list length
    length = len(columna_values) - 1
    counter = 1
    for user in range(length):
        # go to user needing device
        driver.get('HAPPYFOXURL')
        time.sleep(4)

        # finding search bar
        search_query_one = driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/div/div[3]/div/div[1]')
        time.sleep(1)
        search_query_one.click()
        time.sleep(.5)
        search_query_two = driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/div/div[3]/div/div[2]/div/div/input')
        time.sleep(4)

        # enter the student full name
        search_query_two.send_keys(columna_values[counter])
        time.sleep(4)
        search_query_two.send_keys(enter)
        time.sleep(4)

        # finding ticket's url
        url = []
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            url.append(elem.get_attribute("href"))

        # opening ticket
        driver.get(url[0])
        time.sleep(8)

        # add private note for that student
        private_note = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div/div/a[2]')
        private_note.click()
        time.sleep(4)

        private_note_txt = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div[5]/div[1]/div/div/div/div/div')
        private_note_txt.send_keys(newstudent_note)
        time.sleep(4)

        submit_note = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div[5]/div[3]/div[2]/button')
        submit_note.click()
        time.sleep(4)
        counter += 1

    # completed adding notes to relevant tickets
    driver.quit()


if __name__ == '__main__':
    gspreadData()
