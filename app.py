# Takes a LinkedIn URL and creates entry in CSV file (google sheets API)
import imaplib
import email
import os
import service_account as acc
import linker
from datetime import date
from bs4 import BeautifulSoup
import time
import gspread

spreadsheet = acc.Spreadsheet('Applications', 'Main').sheet  # open spreadsheet instance

# Add a row to spreadsheet new application 
# @param: dict of job values
def add_row(job_arr):
    try:
        spreadsheet.append_row(job_arr,value_input_option='USER_ENTERED')
        print('Successfully inserted row..')
    except:
        print('Failed to insert new row.')


# Loop to efficiently add job applications to spreadsheet
while True:
    # Get dict from linkedin link
    job_dict = linker.get_linked()

    print(job_dict)

    # Get current date
    curr_date = date.today()

    # Populate list with returned dict from linker
    job_arr = [job_dict.get('company'),
               job_dict.get('job_title'),
               job_dict.get('location'),
               curr_date.strftime('%m/%d/%Y'),
               job_dict.get('level'),
               job_dict.get('job_url')]

    # Add row to spreadsheet
    add_row(job_arr)

