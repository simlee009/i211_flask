#!/usr/local/bin/python3
# Don't change the line above on Burrow! It has to be on the first line!
#
# This CGI file will allow you to run your Flask app on Burrow, which already
#  has Flask installed. See requirements.txt for the specific versions.
#
# Place this file in the cgi-pub folder of your Burrow account. Make this file 
#  executable for CGI with the following command:
#  
#    chmod u+x ~/cgi-pub/i211_flask.cgi
#
# You will also need to clone your Git repository into your cgi-pub folder with
#  this Git command:
#
#    git clone https://github.iu.edu/[username]/i211_flask.git ~/cgi-pub/i211_flask/
#
#  where [username] is your Burrow/IU username.
#
# If everything is configued correctly, you ought to be able to see your Flask
#  app running at https://cgi.luddy.indiana.edu/~[username]/i211_flask.cgi. 

# Leave this line alone. It tells Python to run as CGI.
from wsgiref.handlers import CGIHandler

# Update the following line or make sure you set up your files and folders to 
#  match ths pattern: 
# 
#    from [Flask folder/Git repo] import [main py file, ie app.py]
#
from i211_flask import app

if __name__ == '__main__':
    # app.app refers to the variable named app (that is set equal to the Flask
    #  application object) in the file app.py, which we imported above.
    CGIHandler().run(app.app)
