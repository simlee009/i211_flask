from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
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
