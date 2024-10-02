from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from joblib import load

app = Flask(__name__)

# Load the trained model
model = load("C:\\Users\\harih\\OneDrive\\Desktop\\PROJECT\\P-2\\ridge_regression_model.joblib")

# Load the AQI data from the Excel file
aqi_data = pd.read_excel('C:\\Users\\harih\\OneDrive\\Desktop\\PROJECT\\P-2\\datasets\\forecast.xlsx')
aqi_data = aqi_data[['City', 'Date', 'AQI']]
aqi_data['Date'] = pd.to_datetime(aqi_data['Date'], errors='coerce')

# Extract unique city names
cities = aqi_data['City'].unique().tolist()

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "Air quality is considered satisfactory, and air pollution poses little or no risk.", "None."
    elif aqi <= 100:
        return "Moderate", "Air quality is acceptable; however, there may be some pollution that poses a moderate health concern for a very small number of individuals who are unusually sensitive to air pollution.", "Unusually sensitive people should consider reducing prolonged or heavy exertion."
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects. The general public is not likely to be affected.", "Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion."
    elif aqi <= 200:
        return "Unhealthy", "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.", "Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion."
    elif aqi <= 300:
        return "Very Unhealthy", "Health alert: everyone may experience more serious health effects.", "Everyone should avoid all outdoor exertion."
    else:
        return "Hazardous", "Health warning of emergency conditions. The entire population is more likely to be affected.", "Everyone should avoid all outdoor exertion."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/current_aqi')
def current_aqi():
    return render_template('current_aqi.html')

@app.route('/forecast')
def forecast():
    return render_template('forecast.html', cities=cities)

@app.route('/about_aqi')
def about_aqi():
    return render_template('about_aqi.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        pm25 = float(request.form['PM2.5'])
        pm10 = float(request.form['PM10'])
        o3 = float(request.form['O3'])
        no2 = float(request.form['NO2'])
        so2 = float(request.form['SO2'])
        co = float(request.form['CO'])

        # Preprocess the input data
        features = np.array([pm25, pm10, o3, no2, so2, co]).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)

        # Round the prediction to two decimal places
        aqi = round(prediction[0], 2)

        # Get AQI category, health implications, and cautionary statement
        category, health_implications, cautionary_statement = get_aqi_category(aqi)

        return render_template('result.html', aqi=aqi, category=category, health_implications=health_implications, cautionary_statement=cautionary_statement)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    try:
        # Get data from request
        data = request.get_json()

        # Preprocess the input data
        features = np.array(data['features']).reshape(1, -1)

        # Make prediction
        prediction = model.predict(features)

        # Round the prediction to two decimal places
        aqi = round(prediction[0], 2)

        # Get AQI category, health implications, and cautionary statement
        category, health_implications, cautionary_statement = get_aqi_category(aqi)

        # Prepare response
        response = {
            'aqi': aqi,
            'category': category,
            'health_implications': health_implications,
            'cautionary_statement': cautionary_statement
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/get_location')
def get_location():
    return render_template('get_location.html')

@app.route('/cities', methods=['GET'])
def get_cities():
    return jsonify(cities)

@app.route('/aqi', methods=['GET'])
def get_aqi():
    city = request.args.get('city')
    if city:
        city_data = aqi_data[aqi_data['City'] == city]
        # Drop rows with missing values
        city_data = city_data.dropna(subset=['AQI'])
        if not city_data.empty:
            monthly_avg_aqi = city_data.groupby(city_data['Date'].dt.to_period('M'))['AQI'].mean().reset_index()
            monthly_avg_aqi['Date'] = monthly_avg_aqi['Date'].dt.strftime('%Y-%m')
            result = monthly_avg_aqi.to_dict(orient='records')
            return jsonify({'data': result})
        else:
            return jsonify({"error": "No data available for the selected city"}), 404
    return jsonify({"error": "City not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
