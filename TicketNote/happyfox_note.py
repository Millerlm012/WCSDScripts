from halo import Halo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
import time
import getpass


# download a txt file to a specific folder in the project directory -> python will keep checking this directory for the file
# check the time -> depending on the time we will either run the program or kill it
def gspreadData():

    # asking user for their happyfox credentials
    user_username = input("Please enter your happyfox username / email: ")
    user_password = getpass.getpass("Please enter your happyfox password: ")

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('PowerschoolReportScript-aafe277a550b.json', scope)
    client = gspread.authorize(creds)

    gc = gspread.authorize(creds)

    # fetching the student information from 'New Student Labels Prep' tab
    # retrieving spreadsheet by url
    itprintinglabels_sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/17c88xz1_kzgLt_QuNPGq7i2xrIYcPgVczHGDp1nUpQo/edit#gid=1836712917')
    # retrieving proper worksheet by name
    newstudentlabelsprep_worksheet = itprintinglabels_sheet.worksheet('Student Labels Prep')
    # fetching all student data from column 'A' and 'B' -> this will retrieve the student's full name and id number
    columna_values = newstudentlabelsprep_worksheet.col_values(1)
    columnb_values = newstudentlabelsprep_worksheet.col_values(2)
    # fetching SN that was given to student as well -> column 'H'
    columnh_values = newstudentlabelsprep_worksheet.col_values(8)

    print('all student names - ' + str(columna_values))
    print('all student id numbers - ' + str(columnb_values))
    print('all serial numbers - ' + str(columnh_values))

    print('-------------------------------------------------------------------')


    createHappyfoxNote(columna_values, columnb_values, columnh_values, user_username, user_password)


def createHappyfoxNote(columna_values, columnb_values, columnh_values, user_username, user_password):

    spinner = Halo(text='In Progress...', spinner='dots')
    spinner.start()
    # initiate chromedriver
    happyfox_link = 'https://ticket.waukeeschools.org/staff/login/?return_to=/staff/tickets/?status=_pending'
    enter = u'\ue007'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options = options)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    # go to happyfox url
    driver.get(happyfox_link)

    # log into happyfox | username
    try:

        print(' | Logging into HappyFox...')
        username_query = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'id_username')))
        # username_query = driver.find_element_by_id('id_username')
        for i in range(len(user_username)):
            username_query.send_keys(user_username[i])
            time.sleep(.5)
            i += 1
        time.sleep(2)

        # log into happyfox | password
        password_query = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'id_password')))
        # password_query = driver.find_element_by_id('id_password')
        for i in range(len(user_password)):
            password_query.send_keys(user_password[i])
            time.sleep(.5)
            i += 1
        password_query.send_keys(enter)
        time.sleep(2)

        # creating variable for range to be 1 less than the length of the list length
        length = len(columna_values) - 1
        counter = 1
        newstudent_note = '- TEST \n- device has been checked out of rm 108 for student: labeled with both student and asset tag: please find the following device in rm-108 on the new student shelf \n- please contact the school and inform them that you will be sending it there via mail \n- Please close ticket once school has received device \n- '
        for user in range(length):
            # go to user needing device
            print(' | Searching for new student ticket for - ' + columna_values[counter])
            driver.get('https://ticket.waukeeschools.org/staff/tickets?view_id=34')
            # time.sleep(4)

            # finding search bar
            search_query_one = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/header/div[2]/div/div[3]/div/div[1]')))

            # search_query_one = driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/div/div[3]/div/div[1]')
            time.sleep(1)
            search_query_one.click()
            time.sleep(1)

            search_query_two = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/header/div[2]/div/div[3]/div/div[2]/div/div/input')))
            # search_query_two = driver.find_element_by_xpath('/html/body/div[3]/header/div[2]/div/div[3]/div/div[2]/div/div/input')
            time.sleep(1)

            # enter the student full name
            search_query_two.send_keys(columna_values[counter])
            time.sleep(4)
            search_query_two.send_keys(enter)
            time.sleep(8)

            # finding ticket url
            url = []
            elems = driver.find_elements_by_xpath("//a[@href]")
            for elem in elems:
                url.append(elem.get_attribute("href"))

            time.sleep(3)

            # opening ticket
            print(' | Opening ticket...')
            driver.get(url[0])
            time.sleep(4)

            # add private note for that student
            print(' | Adding private note to ticket...')
            private_note = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div/div/a[2]')
            private_note.click()
            time.sleep(4)

            private_note_txt = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div[5]/div[1]/div/div/div/div/div')
            private_note_txt.send_keys(newstudent_note + columnh_values[counter])
            time.sleep(4)

            submit_note = driver.find_element_by_xpath('/html/body/div[3]/section/div/section/div/div/div[5]/div[3]/div[2]/button')
            submit_note.click()
            time.sleep(4)
            print(' | Successfully added private note for ' + columna_values[counter] + '!' + ' ' + str(counter) + '/' + str(length) + ' complete!')
            counter += 1

        # completed adding notes to relevant tickets
        spinner.stop()
        print('Completed adding private notes! Please press the purple button on the IT Printing Labels to finalize the new student process.')
        driver.quit()

    except (NoSuchElementException, TimeoutException):
        spinner.stop()
        print('Something went wrong! Ensure you are typing in your username and password correctly! Is Happyfox slow today? \n')

if __name__ == '__main__':
    gspreadData()
