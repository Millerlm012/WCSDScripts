# HappyFox Ticket System - Private Note
About: This program was created to automate adding a specified private note to our tickets that were for our new students.
This private note notified fellow IT members that the new student's device had been labeled and was ready to be set up and given to the student.

How It Works: The program uses the gspread API to gather the data about the new student from a Google Spreadsheet.
It then uses Selenium to go and add the private notes to the proper tickets. This is initialized by someone in IT running the shell script.
As with the PowerschoolReportScript, I used Selenium instead of a dedicated API as this is what I had access to and was able to whip up quickly.

Future Upgrades:

- utilizing the HappyFox API instead of using Selenium
