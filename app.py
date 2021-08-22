from flask import Flask, render_template, request, redirect, url_for
import uuid
import csv

app = Flask(__name__)

PATH_EVENTS = app.root_path + '/events.csv'
PATH_ATTENDEES = app.root_path + '/attendees.csv'

@app.route('/')
def index():
    """Show the home page."""
    return render_template('index.html')

@app.route('/events/')  # Using a trailing slash allows Flask to handle both "/event" and "/event/".
@app.route('/events/<id>')
def events(id=None):
    """Show an event if an ID is specified. Otherwise list all events."""
    if id:
        if id in events.keys():
            event = events[id]
            return render_template('event.html', 
                                    event=event, 
                                    attendees=get_attendees(id))
        else:
            print(f"No event found with id of {id}.")
    # The default is to render the events list.
    return render_template('events.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
@app.route('/edit_event/<id>', methods=['GET', 'POST'])
def set_event(id=None):
    """Create or edit an event. If this function receives POST data, process it.
    If not, render a form that allows the user to enter the data for a new 
    event.
    """
    global events  # We want to make changes to this global varibale.

    if request.method == 'POST':
        if id is None:  # If there's no event ID, create a new event.
            # Generate a random UUID.
            id = str(uuid.uuid4())
        print(f"Event ID {id}.")
        
        # Generate the event info from the form data.
        event = {}
        event['id'] = id
        event['name'] = request.form['event_name']
        event['time'] = request.form['event_date'] + " " + request.form['event_time']
        event['host'] = request.form['event_host']
        events[id] = event

        # Save this data back out to the CSV file.
        write_csv(PATH_EVENTS, events)

        # Once the event has been added, take the user to that event.
        return redirect(url_for('events', id=id))
    else:
        if id is None:
            return render_template('edit_event.html')
        else:
            return render_template('edit_event.html', event=events[id])

@app.route('/delete_event/<id>', methods=['GET', 'POST'])
def delete_event(id=None):
    global events
    global attendees
    if id and id in events:
        del events[id]
        # Gotta delete attendees too.
        event_attendees = get_attendees(id)
        for event_attendee in event_attendees:
            del attendees[event_attendee['id']]
        write_csv(PATH_EVENTS, events)
        write_csv(PATH_ATTENDEES, attendees)
    return redirect(url_for('events'))

@app.route('/about')
def about():
    """About page for B.There."""
    return render_template('about.html')

def read_csv(file_name):
    """Helper function to read in CSV data as a dictionary of dictionaries."""
    results = {}
    try:
        with open(file_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for result in reader:
                results[result["id"]] = result
    except Exception as err:
        print(err)
    return results

def write_csv(file_name, data_dict):
    """Helper function to write data back out to a CSV."""
    try:
        if data_dict and len(data_dict) > 0:
            # Make sure we got a valid dictionary as the data. Then use the 
            #  first row to figure out what keys to use as the field name.
            #  Students could probably just hard-code the field names as a 
            #  parameter instead.
            rows = list(data_dict.values())
            first_row = rows[0]
            if first_row and len(first_row) > 0:
                field_names = list(first_row.keys())
                with open(file_name, mode='w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=field_names)
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(row)
                print('Data saved!')
                return # Return here if we successfully saved the file.
            print('Could not determine field names from first row.')
        print('Invalid data. Changes not saved.')
    except Exception as err:
        print(err)

def get_attendees(event_id):
    """Get all of the attendees for a given event id.

    This function could also be written by looping through the attendees list 
    and building a sublist of the event attendees. That would be more in line
    with the skill level we're shooting for, but the lambda function is just so
    much easier...
    """
    return list(filter(lambda attendee: attendee["eventID"] == event_id, 
                       attendees.values()))

# Read in the events and attendees at app start and keep it in memory, instead 
#  of reading it every single time the events page loads.
events = read_csv(PATH_EVENTS)
attendees = read_csv(PATH_ATTENDEES)

if __name__ == '__main__':
    app.run(debug = True)
