from flask import Flask, render_template, redirect, url_for

import csv  # Used for reading and writing event data via csv.

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events/')
def events():
    events = get_events()
    return render_template('events.html', events=events)

@app.route('/events/<event_id>/')
def event(event_id=None):
    if event_id:
        event_id = int(event_id)
        events = get_events()
        return render_template('event.html', event=events[event_id])
    else:
        return redirect(url_for('events'))

def get_events():
    file_path = app.root_path + '/events.csv'
    results = []
    try:
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            results = list(reader)
    except Exception as err:
        print(err)
    return results

if __name__ == '__main__':
    app.run(debug = True)
