from flask import Flask, render_template
import csv

app = Flask(__name__)

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

def get_attendees(event_id):
    """Get all of the attendees for a given event id.

    This function could also be written by looping through the attendees list 
    and building a sublist of the event attendees. That would be more in line
    with the skill level we're shooting for, but the lambda function is just so
    much easier...
    """
    return filter(lambda attendee: attendee["eventID"] == event_id, 
                  attendees.values())

# Read in the events and attendees at app start and keep it in memory, instead 
#  of reading it every single time the events page loads.
events = read_csv(app.root_path + '/events.csv')
attendees = read_csv(app.root_path + '/attendees.csv')

if __name__ == '__main__':
    app.run(debug = True)
