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
        attendees = database.get_attendees(event_id)
        return render_template('event.html', event=event, attendees=attendees)
    else:
        return redirect(url_for('list_events'))

@app.route('/events/create', methods=['GET', 'POST'])
@app.route('/events/<event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id=None):
    if event_id:
        event_id = int(event_id)

    if request.method == 'POST':
        # Received form data; update the database.
        name = request.form['name']
        date = request.form['date']
        host = request.form['host']
        if event_id:
            database.update_event(event_id, name, date, host)
        else:
            database.insert_event(name, date, host)

        # Return to the list of events.
        return redirect(url_for('list_events'))
    else:
        # Show the event editing form.
        if event_id:
            event = database.get_event(event_id)
        else:
            event = None
        return render_template('event_form.html', event=event)

@app.route('/events/<event_id>/delete')
def delete_event(event_id=None):
    if event_id:
        event_id = int(event_id)
        database.delete_event(event_id)
    return redirect(url_for('list_events'))

@app.route('/events/<event_id>/attendees/add', methods=['GET', 'POST'])
@app.route('/events/<event_id>/attendees/<attendee_id>/edit', methods=['GET', 'POST'])
def edit_attendee(event_id=None, attendee_id=None):
    if event_id:
        event_id = int(event_id)
        if attendee_id:
            attendee_id = int(attendee_id)

        if request.method == 'POST':
            # Got form data. Send it to the database.
            name = request.form['name']
            email = request.form['email']
            comment = request.form['comment']
            if attendee_id:
                database.update_attendee(attendee_id, name, email, comment)
            else:
                database.insert_attendee(event_id, name, email, comment)
            return redirect(url_for('view_event', event_id=event_id))
        else:
            # Show the attendee edit form so the user can enter data.
            event = database.get_event(event_id)
            event_name = event['name']
            if attendee_id:
                attendee = database.get_attendee(attendee_id)
            else:
                attendee = None
            return render_template('attendee_form.html', event_name=event_name, attendee=attendee)
    else:
        return redirect(url_for('list_events'))

@app.route('/events/<event_id>/attendees/<attendee_id>/delete')
def delete_attendee(event_id=None, attendee_id=None):
    if attendee_id:
        attendee_id = int(attendee_id)
        database.delete_attendee(attendee_id)
    if event_id:
        event_id = int(event_id)
        return redirect(url_for('view_event', event_id=event_id))
    else:
        return redirect(url_for('list_events'))

if __name__ == '__main__':
    app.run(debug = True)
