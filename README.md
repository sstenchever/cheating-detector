# Cheating Detector using Google Forms

This is a cheating detector which checks student responses in a Google Form for signs of possible cheating. Teachers will create a Google Form to act as a quiz for students to take. When creating the form, teachers
will be required to create a Google Spreadsheet which is linked to the form. Instructions on how to do that are available [here](https://support.google.com/docs/answer/2917686?hl=en#zippy=%2Cchoose-where-to-store-responses).
Teachers must also make sure that they are collecting email addresses for students taking a quiz and each student must only be able to submit a form once. For each question that is to be checked, teachers will prepend the title of the question with "***".
This identifies that the question should be put through the cheating detector. The main script (cheating_detector.py) can be run directly from the command line on Windows or terminal on Mac OS/Linux. This of course requires that the person running this has Python installed,
preferably Python 3.8 or later.

The script checks for two signals of cheating. The first compares all students responses and looks for matches in those responses. The second will compare each student response to what is found in an online Google search. In order to do this,
we make use of the Google Search API offered by RapidAPI (https://rapidapi.com/apigeek/api/google-search3). In order to use this, you must setup a RapidAPI account and obtain a key for this API. It is free to use for 600 queries per month. For those who need to exceed this, there are paid options available
[here](https://rapidapi.com/apigeek/api/google-search3/pricing).

When cloning the script files, there will be several things that need to be changed in order to get this to work for your Form/Spreadsheet.
1. In gather_respones.py you must update the SAMPLE_SPREADSHEET_ID variable to match the string value of the ID of your Google Spreadsheet. This can be easily located by looking at the end of the URL for your sheet.
It will look like a mix of numbers, and uppercase/lowercase letters.
2. In gather_responses.py you might need to adjust the SAMPLE_RANGE_NAME to match how many rows are in your sheet. The second number, so for '!1:103' would be '103' represents the amount of rows. Each student will take up one row.
So if you had 150 students responding on a quiz, you'll need to make this number probably a little over 150.
3. In cheating_detector.py you will need to update the value of "x-rapidapi-key" to be the string value of the API key you get from RapidAPI for the Google Search API (https://rapidapi.com/apigeek/api/google-search3). 

On a successful run, the results will be written to a text file in the same directory as the script files titled "cheating_detector_output.txt". This is a basic text file used to easily interpret the results of the script.

This project is primarily geared towards giving K-12 teachers a tool they can use to validate the honesty of student submitted work while learning remotely. 
It is not meant to be a sophisticated cheating detection mechanism. There also has not been extensive testing done so if bugs are found, please feel free to submit an issue/pull request. 