from flask import Flask, render_template, redirect, url_for, request

import csv  # Used for reading and writing event data via csv.

app = Flask(__name__)

EVENTS_PATH = app.root_path + '/events.csv'
EVENTS_KEYS = ['name', 'date', 'host']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events/')
def list_events():
    events = get_events()
    return render_template('events.html', events=events)

@app.route('/events/<event_id>/')
def view_event(event_id=None):
    if event_id:
        event_id = int(event_id)
        events = get_events()
        return render_template('event.html', event=events[event_id])
    else:
        return redirect(url_for('list_events'))

@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        events = get_events()
        event = {}
        event['name'] = request.form['name']
        event['date'] = request.form['date']
        event['host'] = request.form['host']
        events.append(event)
        
        # Make sure events are sorted by date.
        events = sorted(events, key=lambda e: e['date'])

        # Write data back out to csv.
        set_events(events)

        # Return to the list of events.
        return redirect(url_for('list_events'))
    else:
        return render_template('create_event.html')

def get_events():
    results = []
    try:
        with open(EVENTS_PATH) as csv_file:
            reader = csv.DictReader(csv_file)
            results = list(reader)
    except Exception as err:
        print(err)
    return results

def set_events(events):
    try:
        with open(EVENTS_PATH, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=EVENTS_KEYS)
            writer.writeheader()
            for event in events:
                writer.writerow(event)
    except Exception as err:
        print(err)

if __name__ == '__main__':
    app.run(debug = True)
