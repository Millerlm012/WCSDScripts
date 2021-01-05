# PowerschoolReport
About: This python program was created as originally, we would have to pull a report from Powerschool, upload it to Google Sheets, and then find the new students to print labels and set up devices for them.
This program elimnated us spending 30-90 minutes completing this manually.
To print labels for new students and set up their devices takes about 15-20 minutes every morning now.

How It Works:
The main python program is initiated by a shell script that is being called at 02:00 am by a crontab.
Once initialized, the program navigates to Powerschool, pulls the report, uploads the data to a Google Spreadsheet utilizing the gspread API, and then the spreadsheet has formulas to take care of the rest.

Notes: Our Systems Admin would have normally completed this work but because he was so busy, I stepped in and did what I could as quickly as possible with what I had access to.
It would've been ideal to use the Powerschool API to pull this data, instead of doing it the primitive way I did with Selenium.

Future Upgrades:
- utilize the Powerschool API to eliminate the need to use Selenium and the webdriver
