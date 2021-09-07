from flask import Flask, render_template, redirect, url_for, request
from os.path import exists

# "app" needs to be defined first so that the database can read its config info.
app = Flask(__name__)

# Set up config keys for database access.
# First load default values, then load the actual values from config.py.
# The actual values in the config file, such as the SECRET_KEY and DB_PASS 
#  should NEVER be included in source control, especially in public repos.
app.config.from_pyfile(app.root_path + '/config_defaults.py')
if exists(app.root_path + '/config.py'):
    app.config.from_pyfile(app.root_path + '/config.py')

import database

EVENTS_PATH = app.root_path + '/events.csv'
EVENTS_KEYS = ['name', 'date', 'host']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events/')
def list_events():
    events = database.get_events()
    return render_template('events.html', events=events)

@app.route('/events/<event_id>/')
def view_event(event_id=None):
    if event_id:
        event_id = int(event_id)
        event = database.get_event(event_id)
        return render_template('event.html', event=event)
    else:
        return redirect(url_for('list_events'))

@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        host = request.form['host']
        database.insert_event(name, date, host)

        # Return to the list of events.
        return redirect(url_for('list_events'))
    else:
        return render_template('create_event.html')

@app.route('/events/<event_id>/delete')
def delete_event(event_id=None):
    if event_id:
        event_id = int(event_id)
        database.delete_event(event_id)
    return redirect(url_for('list_events'))

if __name__ == '__main__':
    app.run(debug = True)
