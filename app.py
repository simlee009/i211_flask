from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    events = read_csv('events.csv')
    return render_template('index.html', events=events)

def read_csv(file_name):
    """Helper function to read in CSV data as a list of dictionaries."""
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        results = list(reader)
    return results

if __name__ == '__main__':
    app.run(debug = True)
