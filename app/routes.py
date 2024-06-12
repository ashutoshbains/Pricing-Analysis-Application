from app import app
from app import main
from app import config
from app import visualgenerator
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/dashboard', methods=['POST'])
def dashboard():
    subcategories = config.get_subcategories()
    chart1 = visualgenerator.get_subcategory_distribution('Ten Thousand Villages','Earrings')
    return render_template('dashboard.html',chart1=chart1,subcategories=subcategories)

# Route to handle refresh subcategory click
@app.route('/refresh_subcategory', methods=['POST'])
def refresh_subcategory():
    data = request.json
    selected_subcategory = data['subcategory']
    main.update_data(selected_subcategory)
    return 'Refresh completed'


@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    print('UPDATING DASHBOARD')
    return 'UPDATE COMPLETED'

# Route to handle store list population
@app.route('/get_stores', methods=['POST'])
def get_stores_route():
    selected_subcategory = request.json['subcategory']
    stores = main.get_scrapers_for_subcategory(selected_subcategory,get_names=True)
    return jsonify({'stores': stores})