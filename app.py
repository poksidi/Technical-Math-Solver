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
            "nim": "24-071", 
            "role": "Full Stack Developer & Project Manager"
        },
        {
            "nama": "Ahmad Maulana Kafiyahya", 
            "nim": "24-002", 
            "role": "Frontend Developer & Technical Content"
        },
        {
            "nama": "Anindya Fausta Adhidaiva Cetta", 
            "nim": "24-041", 
            "role": "Mathematical Content"
        }
    ],
    "institusi": "Pendidikan Matematika, FKIP, Universitas Jember",
    "repository": "https://github.com/poksidi/Technical-Math-Solver"
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
    calculation['id'] = len(calculations) + 1
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

# API Routes for calculations
@app.route('/api/convert-units', methods=['POST'])
def convert_units():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'success': False})
        
        value = float(data.get('value', 0))
        from_unit = data.get('from_unit', '')
        to_unit = data.get('to_unit', '')
        category = data.get('category', 'length')
        
        # Conversion factors
        conversions = {
            'length': {
                'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
                'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
            },
            'mass': {
                'mg': 0.000001, 'g': 0.001, 'kg': 1.0, 'ton': 1000.0,
                'oz': 0.0283495, 'lb': 0.453592
            },
            'temperature': {
                'c': 'celsius', 'f': 'fahrenheit', 'k': 'kelvin'
            }
        }
        
        result = 0.0
        
        if category == 'temperature':
            # Temperature conversion
            if from_unit == 'c' and to_unit == 'f':
                result = (value * 9/5) + 32
            elif from_unit == 'c' and to_unit == 'k':
                result = value + 273.15
            elif from_unit == 'f' and to_unit == 'c':
                result = (value - 32) * 5/9
            elif from_unit == 'f' and to_unit == 'k':
                result = (value - 32) * 5/9 + 273.15
            elif from_unit == 'k' and to_unit == 'c':
                result = value - 273.15
            elif from_unit == 'k' and to_unit == 'f':
                result = (value - 273.15) * 9/5 + 32
            else:
                result = value  # Same unit
        else:
            # Standard conversion
            if from_unit in conversions[category] and to_unit in conversions[category]:
                base_value = value * conversions[category][from_unit]
                result = base_value / conversions[category][to_unit]
            else:
                return jsonify({'error': 'Invalid units for category', 'success': False})
        
        calculation = {
            'type': 'unit_conversion',
            'input': f"{value} {from_unit}",
            'output': f"{result:.4f} {to_unit}",
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
        save_calculation(calculation)
        
        return jsonify({
            'result': round(result, 6), 
            'formatted_result': f"{result:.4f}",
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': f'Conversion error: {str(e)}', 'success': False})

@app.route('/api/electrical-calc', methods=['POST'])
def electrical_calc():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'success': False})
        
        calc_type = data.get('type', '')
        
        if calc_type == 'ohms_law':
            # Ohm's Law: V = I * R, P = V * I
            voltage = data.get('voltage')
            current = data.get('current')
            resistance = data.get('resistance')
            
            result = {}
            
            if voltage is not None and current is not None:
                voltage = float(voltage)
                current = float(current)
                resistance = voltage / current
                power = voltage * current
                result = {
                    'resistance': round(resistance, 4),
                    'power': round(power, 4)
                }
            elif voltage is not None and resistance is not None:
                voltage = float(voltage)
                resistance = float(resistance)
                current = voltage / resistance
                power = voltage * current
                result = {
                    'current': round(current, 4),
                    'power': round(power, 4)
                }
            elif current is not None and resistance is not None:
                current = float(current)
                resistance = float(resistance)
                voltage = current * resistance
                power = voltage * current
                result = {
                    'voltage': round(voltage, 4),
                    'power': round(power, 4)
                }
            else:
                return jsonify({'error': 'Provide any two values', 'success': False})
            
            calculation = {
                'type': 'electrical_ohms_law',
                'input': data,
                'output': result,
                'timestamp': datetime.now().isoformat()
            }
            save_calculation(calculation)
            
            return jsonify({'result': result, 'success': True})
            
        elif calc_type == 'series_parallel':
            resistors = [float(r.strip()) for r in data.get('resistors', '').split(',') if r.strip()]
            circuit_type = data.get('circuit_type', 'series')
            
            if not resistors:
                return jsonify({'error': 'No resistors provided', 'success': False})
            
            if circuit_type == 'series':
                total = sum(resistors)
            else:  # parallel
                total = 1 / sum(1/r for r in resistors)
            
            result = {'total_resistance': round(total, 4)}
            
            calculation = {
                'type': 'electrical_circuit',
                'input': data,
                'output': result,
                'timestamp': datetime.now().isoformat()
            }
            save_calculation(calculation)
            
            return jsonify({'result': result, 'success': True})
        else:
            return jsonify({'error': 'Invalid calculation type', 'success': False})
    
    except Exception as e:
        return jsonify({'error': f'Electrical calculation error: {str(e)}', 'success': False})

@app.route('/api/material-calc', methods=['POST'])
def material_calc():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'success': False})
        
        calc_type = data.get('type', '')
        
        if calc_type == 'volume_weight':
            length = float(data.get('length', 0))
            width = float(data.get('width', 0))
            height = float(data.get('height', 0))
            density = float(data.get('density', 0))
            
            volume = length * width * height
            weight = volume * density
            
            result = {
                'volume': round(volume, 4),
                'weight': round(weight, 4)
            }
            
            calculation = {
                'type': 'material_volume_weight',
                'input': data,
                'output': result,
                'timestamp': datetime.now().isoformat()
            }
            save_calculation(calculation)
            
            return jsonify({'result': result, 'success': True})
            
        elif calc_type == 'beam_stress':
            load = float(data.get('load', 0))
            length = float(data.get('length', 0))
            width = float(data.get('width', 0))
            height = float(data.get('height', 0))
            
            # Simple beam stress calculation (bending stress)
            area = width * height
            moment = (load * length) / 4  # Simplified for center load
            section_modulus = (width * height**2) / 6
            stress = moment / section_modulus if section_modulus != 0 else 0
            
            result = {
                'stress': round(stress, 4),
                'area': round(area, 4),
                'section_modulus': round(section_modulus, 4)
            }
            
            calculation = {
                'type': 'material_beam_stress',
                'input': data,
                'output': result,
                'timestamp': datetime.now().isoformat()
            }
            save_calculation(calculation)
            
            return jsonify({'result': result, 'success': True})
        else:
            return jsonify({'error': 'Invalid calculation type', 'success': False})
    
    except Exception as e:
        return jsonify({'error': f'Material calculation error: {str(e)}', 'success': False})

@app.route('/api/geometry-calc', methods=['POST'])
def geometry_calc():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'success': False})
        
        shape = data.get('shape', '')
        
        if shape == 'rectangle':
            length = float(data.get('length', 0))
            width = float(data.get('width', 0))
            area = length * width
            perimeter = 2 * (length + width)
            result = {'area': area, 'perimeter': perimeter}
            
        elif shape == 'circle':
            radius = float(data.get('radius', 0))
            area = math.pi * radius ** 2
            circumference = 2 * math.pi * radius
            result = {'area': area, 'circumference': circumference}
            
        elif shape == 'triangle':
            base = float(data.get('base', 0))
            height = float(data.get('height', 0))
            side1 = float(data.get('side1', base))
            side2 = float(data.get('side2', base))
            area = 0.5 * base * height
            perimeter = base + side1 + side2
            result = {'area': area, 'perimeter': perimeter}
            
        elif shape == 'cylinder':
            radius = float(data.get('radius', 0))
            height = float(data.get('height', 0))
            volume = math.pi * radius ** 2 * height
            surface_area = 2 * math.pi * radius * (radius + height)
            result = {'volume': volume, 'surface_area': surface_area}
            
        else:
            return jsonify({'error': 'Invalid shape', 'success': False})
        
        calculation = {
            'type': f'geometry_{shape}',
            'input': data,
            'output': result,
            'timestamp': datetime.now().isoformat()
        }
        save_calculation(calculation)
        
        return jsonify({'result': {k: round(v, 4) for k, v in result.items()}, 'success': True})
    
    except Exception as e:
        return jsonify({'error': f'Geometry calculation error: {str(e)}', 'success': False})

@app.route('/api/history')
def get_history():
    calculations = load_calculations()
    return jsonify(calculations[-10:])  # Return last 10 calculations

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('static/data', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    app.run(debug=True, port=5000)

@app.route('/api/geometry-calc', methods=['POST'])
def geometry_calc():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'success': False})
        
        shape = data.get('shape', '')
        
        if shape == 'rectangle':
            length = float(data.get('length', 0))
            width = float(data.get('width', 0))
            area = length * width
            perimeter = 2 * (length + width)
            result = {'area': area, 'perimeter': perimeter}
            
        elif shape == 'circle':
            radius = float(data.get('radius', 0))
            area = math.pi * radius ** 2
            circumference = 2 * math.pi * radius
            result = {'area': area, 'circumference': circumference}
            
        elif shape == 'triangle':
            base = float(data.get('base', 0))
            height = float(data.get('height', 0))
            side1 = float(data.get('side1', base))
            side2 = float(data.get('side2', base))
            area = 0.5 * base * height
            perimeter = base + side1 + side2
            result = {'area': area, 'perimeter': perimeter}
            
        elif shape == 'cylinder':
            radius = float(data.get('radius', 0))
            height = float(data.get('height', 0))
            volume = math.pi * radius ** 2 * height
            surface_area = 2 * math.pi * radius * (radius + height)
            result = {'volume': volume, 'surface_area': surface_area}
            
        elif shape == 'cube':
            side = float(data.get('side', 0))
            volume = side ** 3
            surface_area = 6 * (side ** 2)
            result = {'volume': volume, 'surface_area': surface_area}
            
        elif shape == 'sphere':
            radius = float(data.get('radius', 0))
            volume = (4/3) * math.pi * (radius ** 3)
            surface_area = 4 * math.pi * (radius ** 2)
            result = {'volume': volume, 'surface_area': surface_area}
            
        else:
            return jsonify({'error': 'Invalid shape', 'success': False})
        
        calculation = {
            'type': f'geometry_{shape}',
            'input': data,
            'output': result,
            'timestamp': datetime.now().isoformat()
        }
        save_calculation(calculation)
        
        return jsonify({'result': {k: round(v, 4) for k, v in result.items()}, 'success': True})
    
    except Exception as e:
        return jsonify({'error': f'Geometry calculation error: {str(e)}', 'success': False})

