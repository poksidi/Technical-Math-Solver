from flask import Flask, render_template, request, jsonify, session
import json
import math
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'technical_math_secret_key'

# Data storage file
DATA_FILE = 'static/data/calculations.json'

# Team information data
TEAM_INFO = {
    "nama_kelompok": "TEKNIK",
    "aplikasi": "Technical Math Solver", 
    "anggota": [
        {
            "nama": "Tedy Bali Ragila", 
            "nim": "24-001", 
            "role": "Backend Developer & Project Manager"
        },
        {
            "nama": "Ahmad Maulana Kafiyahya", 
            "nim": "24-002", 
            "role": "Frontend Developer & UI/UX Designer"
        },
        {
            "nama": "Anindya Fausta", 
            "nim": "24-003", 
            "role": "Content Specialist & Tester"
        }
    ],
    "institusi": "Pendidikan Matematika, FKIP, Universitas Jember",
    "repository": "https://github.com/kelompok12-technical/technical-math-solver"
}

def load_calculations():
    """Load previous calculations from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_calculation(calculation):
    """Save calculation to JSON file"""
    calculations = load_calculations()
    calculations.append(calculation)
    with open(DATA_FILE, 'w') as f:
        json.dump(calculations[-20:], f, indent=2)  # Keep last 20 calculations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team-info')
def team_info():
    return render_template('team_info.html', team_info=TEAM_INFO)

@app.route('/api/team-data')
def team_data():
    return jsonify(TEAM_INFO)

# ... (routes yang sudah ada sebelumnya tetap sama) ...

@app.route('/unit-converter')
def unit_converter():
    return render_template('unit_converter.html')

@app.route('/electrical')
def electrical():
    return render_template('electrical.html')

@app.route('/materials')
def materials():
    return render_template('materials.html')

@app.route('/geometry')
def geometry():
    return render_template('geometry.html')

# ... (API routes yang sudah ada sebelumnya) ...

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('static/data', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=True, port=5000)