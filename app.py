import os
import logging
from flask import Flask, render_template, jsonify
from data_processor import SurveyDataProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize data processor
data_processor = SurveyDataProcessor()

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        # Get processed survey data
        survey_data = data_processor.get_survey_insights()
        return render_template('index.html', data=survey_data)
    except Exception as e:
        logging.error(f"Error loading dashboard: {e}")
        return render_template('index.html', data={
            'error': 'Failed to load survey data. Please try again later.'
        })

@app.route('/api/chart-data')
def get_chart_data():
    """API endpoint for chart data"""
    try:
        chart_data = data_processor.get_chart_data()
        return jsonify(chart_data)
    except Exception as e:
        logging.error(f"Error getting chart data: {e}")
        return jsonify({'error': 'Failed to load chart data'}), 500

@app.route('/api/request-data', methods=['POST'])
def request_full_data():
    """Handle requests for complete survey data"""
    # In a real application, this would send an email or create a ticket
    logging.info("Full data request received")
    return jsonify({'message': 'Your request has been submitted. You will receive the complete data within 24 hours.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
