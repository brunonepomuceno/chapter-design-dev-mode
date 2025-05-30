import os
import logging
from flask import Flask, render_template, jsonify, send_file
from data_processor import SurveyDataProcessor
from pdf_generator import PDFReportGenerator

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

@app.route('/api/download-report')
def download_report():
    """Generate and download PDF report"""
    try:
        pdf_generator = PDFReportGenerator()
        pdf_buffer = pdf_generator.generate_pdf_report()
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'relatorio_dev_mode_{data_processor.get_survey_insights()["report_date"].replace(" de ", "_").replace(" ", "_")}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        logging.error(f"Error generating PDF report: {e}")
        return jsonify({'error': 'Failed to generate PDF report'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
