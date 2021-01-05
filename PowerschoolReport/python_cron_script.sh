#!/bin/bash

# NOTES:
# script to initialize the python venv and run the python script
# on first time use -> ensure that you make the script executable with chmod +x 'script name'

# navigates to directory where script and venv are found
cd /Users/lmiller/PythonProjects/powerschoolReportScript

# initializes venv
source env/bin/activate

# starts python script
python3 main.py

# deactivates venv once script is complete
deactivate
