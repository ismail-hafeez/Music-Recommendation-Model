
from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import os

app = Flask(__name__, static_url_path='/static')

# Read the CSV file into a DataFrame
df = pd.read_csv('/home/hdoop/Downloads/data2.csv')

count = 0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore_html():
    return render_template('explore.html')

@app.route('/getStarted')
def getStarted_html():
    return render_template('getStarted.html',table=df)


@app.route('/history')
def history_html():
    try:
        df_read = pd.read_csv('audio_data.csv')
        print("Data read successfully:")
        print(df_read)
    except Exception as e:
        print("Error reading CSV file:", e)
        df_read = None  # Define df_read as None if an error occurs
    return render_template('history.html', table1=df_read)

# Route to process the form
@app.route('/process', methods=['POST'])
def process_form():
    selected_rows = request.form.getlist('selected_rows')  # Get the list of selected rows

    # Process the selected rows and save the data
    selected_data = []
    for row_str in selected_rows:
        row_values = row_str.split(',')  # Split the string into separate values
        selected_data.append({
            'ID': row_values[0],
            'Artist': row_values[1],
            'Album': row_values[2]
        })
    
    # Transform the data into a DataFrame
    df_temp = pd.DataFrame(selected_data, columns=['ID', 'Artist', 'Album'])

    # Saving to CSV
    header = not os.path.exists('audio_data.csv')  # Determine whether to include the header
    df_temp.to_csv('audio_data.csv', index=False, mode='a', header=header)

    # Read from CSV
    try:
        df_read = pd.read_csv('audio_data.csv')
        print("Data read successfully:")
        print(df_read)
    except Exception as e:
        print("Error reading CSV file:", e)

    return render_template('history.html', table1=df_read)


if __name__ == '__main__':
    app.run(debug=True)