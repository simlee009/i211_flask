#!/usr/local/bin/python3
# Don't change the line above on Burrow! It has to be on the first line!
#
# This CGI file will allow you to run your Flask app on Burrow, which already
#  has Flask installed. See requirements.txt for the specific versions.
#
# Place this file in the cgi-pub folder of your Burrow account.
#
# If everything is configued correctly, you ought to be able to see your Flask
#  app running at https://cgi.luddy.indiana.edu/~[username]/i211_flask.cgi, 
#  where [username] is your Burrow/IU username.

from wsgiref.handlers import CGIHandler

# This line adds the i22_flask folder to the path so that imports will work.
import sys
sys.path.append('i211_flask')

# Update the following line or make sure you set up your files and folders to 
#  match: from [Flask folder/Git repo] import [main py file, ie app.py]
from i211_flask import app

if __name__ == '__main__':
    # app.app translates to the variable named app (that points to the Flask
    #  application object) in the file app.py, which was imported above.
    CGIHandler().run(app.app)
