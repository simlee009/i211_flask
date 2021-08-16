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
        # Once we get an id, we need to try to match it to an event in our list.
        # Instead of using some fancy Python, just do a simple loop.
        for event in events:
            if event["id"] == id:
                # Found the id!
                return render_template('event.html', event=event)
        print(f"No event found with id of {id}.")
    # The default is to render the events list.
    return render_template('events.html', events=events)

def read_csv(file_name):
    """Helper function to read in CSV data as a list of dictionaries."""
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        results = list(reader)
    return results

# Read in the events at app start and keep it in memory, instead of reading it
#  every single time the events page loads.
events = read_csv('events.csv')

if __name__ == '__main__':
    app.run(debug = True)
