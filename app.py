from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import pandas as pd
from model import predict_intolerance
import mysql.connector

app = Flask(__name__, static_url_path='/static')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'patient_result'

def create_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

@app.route('/form')
def form():
    return render_template('form.html')
@app.route('/')
def index():
    return render_template('form.html')
@app.route('/search', methods=['POST'])
def filter():
    # Get the search query from the form
    search_query = request.form.get('search_query')
    # Perform the database query
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT Full_name, Result, Update_date FROM patient WHERE Full_name LIKE '%' %s '%'"
    cursor.execute(query, (search_query,))
    results = cursor.fetchall()
    connection.close()
    return render_template('search.html', data=results)

@app.route('/search', methods=['GET'])
def search():
     #Data base connection
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT Full_name, Result, Update_date FROM patient')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('search.html', data=data)

@app.route('/redirect_to_search', methods=['POST'])
def redirect_to_search():
    return redirect(url_for('search'))


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    gender = request.form.get('gender')
    age = request.form.get('age')
    illness_type = request.form.getlist('illness_type')
    personal_illness = request.form.get('personal_illness')
    hereditary_illness = request.form.get('hereditary_illness')
    atopy_type = request.form.getlist('atopy_type')
    tabac = request.form.get('tabac')
    alcool = request.form.get('alcool')
    event = request.form.getlist('event')

     # Check for empty inputs
    errors = {}
    if not gender:
        errors['gender'] = 'Please select a gender.'
    if not age:
        errors['age'] = 'Please enter an age.'
    elif not age.isdigit():
        errors['age'] = 'Age must be a number.'
    elif int(age) < 1 or int(age) > 120:
        errors['age'] = 'Age must be between 1 and 120.'
    if not illness_type:
        errors['illness_type'] = 'Please select at least one illness type.'
    if not personal_illness:
        errors['personal_illness'] = 'Please enter personal illness information.'
    if not hereditary_illness:
        errors['hereditary_illness'] = 'Please enter hereditary illness information.'
    if not atopy_type:
        errors['atopy_type'] = 'Please select at least one atopy type.'
    if not tabac:
        errors['tabac'] = 'Please select tabac information.'
    if not alcool:
        errors['alcool'] = 'Please select alcohol information.'
    if not event:
        errors['event'] = 'Please enter event information.'
    if not name:
        errors['name'] = 'Please enter patient name.'


    # If there are errors, render the form template with error messages
    if errors:
        return render_template('form.html', errors=errors)

    
    # Age category
    if age.isdigit():
        age = int(age)
    if age in range(1, 20):
        New_age = '100000'

    elif age in range(21,30):
        New_age = '010000'

    elif age in range (31,40):
        New_age = '001000'

    elif age in range (41,60):
        New_age = '000100'

    elif age in range (61,70):
        New_age = '000010'

    else:
        New_age = '000001'  

    # PRECIS_IM BOXES VALUES
    if '1' in illness_type:
         IM1_value = 1
    else:
         IM1_value = 0

    if '2' in illness_type:
         IM2_value = 1
    else:
         IM2_value = 0

    if '3' in illness_type:
         IM3_value = 1
    else:
        IM3_value = 0

    if '4' in illness_type:
        IM4_value = 1 
    else:
        IM4_value = 0
    
    if '5' in illness_type:
        IM1_value = '?'
        IM2_value = '?'
        IM3_value = '?'
        IM4_value = '?'
    else:
        IM5_value = 0
   

    # PRECIS_ATOP BOXES VALUES
    if '1' in atopy_type:
        ATOPY1_value = 1
    else:
        ATOPY1_value = 0

    if '2' in atopy_type:
        ATOPY2_value = 1
    else:
        ATOPY2_value = 0

    if '3' in atopy_type:
        ATOPY3_value = 1
    else:
        ATOPY3_value = 0

    if '4' in atopy_type:
        ATOPY4_value = 1 
    else:
        ATOPY4_value = 0

    if '5' in atopy_type:
        ATOPY5_value = 1 
    else:
        ATOPY5_value = 0
    
    if '6' in atopy_type:
        ATOPY1_value = '?'
        ATOPY2_value = '?'
        ATOPY3_value = '?'
        ATOPY4_value = '?'
        ATOPY5_value = '?'
    else:
        ATOPY6_value = 0


    # EVENT BOXES VALUES
    if '1' in event:
        EVENT1_value = 1
    else:
        EVENT1_value = 0

    if '2' in event:
        EVENT2_value = 1
    else:
        EVENT2_value = 0

    if '3' in event:
        EVENT3_value = 1
    else:
        EVENT3_value = 0

    if '4' in event:
        EVENT4_value = 1 
    else:
        EVENT4_value = 0

    if '5' in event:
        EVENT5_value = 1 
    else:
        EVENT5_value = 0

    if '6' in event:
        EVENT6_value = 1 
    else:
        EVENT6_value = 0

    if '7' in event:
        EVENT7_value = 1 
    else:
        EVENT7_value = 0
    
    if '8' in event:
        EVENT1_value = '?'
        EVENT2_value = '?'
        EVENT3_value = '?'
        EVENT4_value = '?'
        EVENT5_value = '?'
        EVENT6_value = '?'
        EVENT7_value = '?'
    else:
        EVENT8_value = 0
    

    # Define the form data as a dictionary
    form_data = {
        'Sexe': gender,
        'tranche_dage_0': New_age[0] ,
        'tranche_dage_1': New_age[1] ,
        'tranche_dage_2': New_age[2] ,
        'tranche_dage_3': New_age[3] ,
        'tranche_dage_4': New_age[4] ,
        'tranche_dage_5': New_age[5] ,
        'ATCD': [1] ,
        'PRÉCIS_IM1': [IM1_value],
        'PRÉCIS_IM2': [IM2_value],
        'PRÉCIS_IM3': [IM3_value],
        'PRÉCIS_IM4': [IM4_value],
        'Atopie_P': personal_illness,
        'PRÉCIS_ATOP_1': [ATOPY1_value],
        'PRÉCIS_ATOP_2': [ATOPY2_value],
        'PRÉCIS_ATOP_3': [ATOPY3_value],
        'PRÉCIS_ATOP_4': [ATOPY4_value],
        'PRÉCIS_ATOP_5': [ATOPY5_value],
        'Atopie_F': hereditary_illness,
        'Tabac': tabac,
        'Alcool': alcool,
        'M_NM_NC': [-1],
        'EV_UNIFORM_1': [EVENT1_value],
        'EV_UNIFORM_2': [EVENT2_value],
        'EV_UNIFORM_3': [EVENT3_value],
        'EV_UNIFORM_4': [EVENT4_value],
        'EV_UNIFORM_5': [EVENT5_value],
        'EV_UNIFORM_6': [EVENT6_value],
        'EV_UNIFORM_7': [EVENT7_value],
    }

    # Read the existing Excel file
    try:
        df_old = pd.read_excel('form_data.xlsx', sheet_name='Sheet1')
    except FileNotFoundError:
        df_old = pd.DataFrame()

    # Create a DataFrame from the form data
    df_new = pd.DataFrame(form_data, index=[len(df_old)])

    # Concatenate the old and new DataFrames
    df = pd.concat([df_old, df_new])

    # Write the concatenated DataFrame to the Excel file
    with pd.ExcelWriter('form_data.xlsx', mode='w') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Prediction message
       # print (predict_intolerance())
    type_response = predict_intolerance()

    if type_response[0] < 1:
     prediction_str = "Patient does not have medical intolerance."
    else : 
      prediction_str = "Patient have medical intolerance."

    


    # Return the prediction as a JSON object
    response = prediction_str
    #Data base connection
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO patient (Full_name, Gender, Age, Event, Therapeutic_Classification, Personal_illness, Hereditary_illness, Atopy_type, Tabac, Alcohol, Result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (name, gender, age, json.dumps(event), json.dumps(illness_type), personal_illness, hereditary_illness, json.dumps(atopy_type), tabac, alcool, prediction_str))
    connection.commit()
    cursor.close()
    connection.close()

    return render_template('success.html',response=response)

if __name__ == '__main__':
    app.run(debug=True)
