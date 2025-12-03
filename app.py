from flask import Flask, render_template, request
import json
import math

# --- 1. INISIALISASI APP (WAJIB DI ATAS) ---
app = Flask(__name__)
app.secret_key = 'teknik_jaya_123'

# --- 2. DATA REFERENSI ---

# --- UPDATE DATA REFERENSI (LENGKAP) ---
TEAM_INFO = {
    "nama_kelompok": "TEKNIK",
    "divisi": "SMK",
    "aplikasi": "Technical Math Solver",
    "deskripsi": "Aplikasi Edutainment Matematika Teknik",
    "institusi": "Pendidikan Matematika, FKIP, Universitas Jember",
    "repository": "https://github.com/poksidi/Technical-Math-Solver",
    "anggota": [
        {"nama": "Tedy Bali Ragila", "nim": "24-071", "role": "Full Stack Developer, Math & Technical Content, & Project Manager", "color": "primary"},
        {"nama": "Ahmad Maulana Kafiyahya", "nim": "24-128", "role": "Frontend Developer & Technical Dev", "color": "danger"},
        {"nama": "Anindya Fausta Adhidaiva Cetta", "nim": "24-041", "role": "Mathematical Content", "color": "info"}
    ]
}

# --- DATA MATERIAL LENGKAP (Density dalam kg/m³) ---
MATERIALS_DATA = {
    'carbon_steel': {'name': 'Baja Karbon (Carbon Steel)', 'density': 7850},
    'stainless_304': {'name': 'Stainless Steel 304', 'density': 7900},
    'stainless_316': {'name': 'Stainless Steel 316', 'density': 7980},
    'aluminium_6061': {'name': 'Aluminium 6061', 'density': 2700},
    'brass': {'name': 'Kuningan (Brass)', 'density': 8500},
    'bronze': {'name': 'Perunggu (Bronze)', 'density': 8800},
    'copper': {'name': 'Tembaga (Copper)', 'density': 8960},
    'cast_iron': {'name': 'Besi Cor (Cast Iron)', 'density': 7200},
    'titanium': {'name': 'Titanium', 'density': 4500},
    'gold': {'name': 'Emas Murni', 'density': 19320}
}

# Data Konversi (Untuk fitur Konversi Dinamis)
UNIT_DATA = {
    'Panjang': {
        'Meter (m)': 1,
        'Kilometer (km)': 1000,
        'Centimeter (cm)': 0.01,
        'Millimeter (mm)': 0.001,
        'Micrometer (µm)': 0.000001,
        'Nanometer (nm)': 0.000000001,
        'Mile (mi)': 1609.34,
        'Yard (yd)': 0.9144,
        'Foot (ft)': 0.3048,
        'Inch (in)': 0.0254
    },
    'Massa': {
        'Kilogram (kg)': 1,
        'Gram (g)': 0.001,
        'Milligram (mg)': 0.000001,
        'Ton (t)': 1000,
        'Quintal (kw)': 100,
        'Pound (lbs)': 0.453592,
        'Ounce (oz)': 0.0283495
    },
    'Waktu': {
        'Detik (s)': 1,
        'Menit (min)': 60,
        'Jam (hr)': 3600,
        'Hari (day)': 86400,
        'Minggu (wk)': 604800,
        'Tahun (yr)': 31536000
    },
    'Luas': {
        'Meter Persegi (m²)': 1,
        'Kilometer Persegi (km²)': 1000000,
        'Hektar (ha)': 10000,
        'Are (a)': 100,
        'Kaki Persegi (ft²)': 0.092903
    },
    'Volume': {
        'Meter Kubik (m³)': 1,
        'Liter (L)': 0.001,
        'Milliliter (mL)': 0.000001,
        'Gallon US (gal)': 0.00378541
    },
    'Kecepatan': {
        'Meter/Detik (m/s)': 1,
        'Km/Jam (km/h)': 0.277778,
        'Miles/Hour (mph)': 0.44704
    },
    'Tekanan': {
        'Pascal (Pa)': 1,
        'Bar': 100000,
        'PSI': 6894.76,
        'Atmosphere (atm)': 101325
    },
    'Daya': {
        'Watt (W)': 1,
        'Kilowatt (kW)': 1000,
        'Horsepower (HP)': 745.7
    },
    'Energi': {
        'Joule (J)': 1,
        'Kilojoule (kJ)': 1000,
        'Kalori (cal)': 4.184,
        'Kilocalorie (kcal)': 4184,
        'Watt Hour (Wh)': 3600
    }
}

# --- 3. ROUTES (HALAMAN) ---
@app.route('/')
def home():
    return render_template('index.html', team=TEAM_INFO)

@app.route('/team')
def team_page():
    return render_template('team.html', team=TEAM_INFO)

# --- FITUR LISTRIK (DINAMIS: KATEGORI -> RUMUS) ---
@app.route('/electric', methods=['GET', 'POST'])
def electric():
    result = None
    
    # Data Menu untuk Dropdown (Dikirim ke HTML/JS)
    # Struktur: Kategori -> { Kode_Rumus: { label: Nama_Rumus, inputs: [Label_Input1, Label_Input2] } }
    ELEC_MENU = {
        'Hukum Ohm & Daya': {
            'ohm_v': {'label': 'Cari Tegangan (V = I × R)', 'inputs': ['Arus (Ampere)', 'Hambatan (Ohm)']},
            'ohm_i': {'label': 'Cari Arus (I = V / R)', 'inputs': ['Tegangan (Volt)', 'Hambatan (Ohm)']},
            'ohm_r': {'label': 'Cari Hambatan (R = V / I)', 'inputs': ['Tegangan (Volt)', 'Arus (Ampere)']},
            'pow_p': {'label': 'Cari Daya (P = V × I)', 'inputs': ['Tegangan (Volt)', 'Arus (Ampere)']}
        },
        'Rangkaian Seri (2 Resistor)': {
            'seri_r': {'label': 'Hambatan Total (R_total = R1 + R2)', 'inputs': ['Resistor 1 (Ohm)', 'Resistor 2 (Ohm)']},
            'seri_v': {'label': 'Tegangan Total (V_total = V1 + V2)', 'inputs': ['Tegangan 1 (Volt)', 'Tegangan 2 (Volt)']}
        },
        'Rangkaian Paralel (2 Resistor)': {
            'para_r': {'label': 'Hambatan Total (1/Rt = 1/R1 + 1/R2)', 'inputs': ['Resistor 1 (Ohm)', 'Resistor 2 (Ohm)']},
            'para_i': {'label': 'Arus Total (I_total = I1 + I2)', 'inputs': ['Arus Cabang 1 (A)', 'Arus Cabang 2 (A)']}
        }
    }

    # Variabel untuk menampung input user agar tidak hilang saat reload
    s_cat = ''
    s_form = ''
    val1 = ''
    val2 = ''

    if request.method == 'POST':
        try:
            # Ambil data dari form
            category = request.form.get('category')
            formula = request.form.get('formula')
            v1 = float(request.form.get('val1'))
            v2 = float(request.form.get('val2'))
            
            # Simpan state untuk dikembalikan ke template
            s_cat = category
            s_form = formula
            val1 = v1
            val2 = v2

            # --- LOGIKA PERHITUNGAN ---
            
            # 1. HUKUM OHM & DAYA
            if formula == 'ohm_v':
                res = v1 * v2
                result = f"Tegangan (V) = {res:.2f} Volt"
            elif formula == 'ohm_i':
                res = v1 / v2
                result = f"Arus (I) = {res:.2f} Ampere"
            elif formula == 'ohm_r':
                res = v1 / v2
                result = f"Hambatan (R) = {res:.2f} Ohm"
            elif formula == 'pow_p':
                res = v1 * v2
                result = f"Daya (P) = {res:.2f} Watt"

            # 2. RANGKAIAN SERI
            elif formula == 'seri_r':
                res = v1 + v2
                result = f"Hambatan Total Seri = {res:.2f} Ohm"
            elif formula == 'seri_v':
                res = v1 + v2
                result = f"Tegangan Sumber Total = {res:.2f} Volt"

            # 3. RANGKAIAN PARALEL
            elif formula == 'para_r':
                # Rumus R Paralel (2 Resistor): (R1 * R2) / (R1 + R2)
                res = (v1 * v2) / (v1 + v2)
                result = f"Hambatan Total Paralel = {res:.2f} Ohm"
            elif formula == 'para_i':
                res = v1 + v2
                result = f"Arus Total Masuk = {res:.2f} Ampere"

        except (ValueError, ZeroDivisionError, TypeError):
            result = "Error: Input tidak valid atau pembagian nol."

    return render_template('electric.html', 
                           result=result, 
                           team=TEAM_INFO, 
                           elec_menu=ELEC_MENU,
                           s_cat=s_cat, s_form=s_form, v1=val1, v2=val2)

# --- FITUR GEOMETRI (2D & 3D LENGKAP) ---
@app.route('/geometry', methods=['GET', 'POST'])
def geometry():
    result = None
    
    # MENU GEOMETRI LENGKAP
    GEO_MENU = {
        'Bangun Datar (2D)': {
            'square': {'label': 'Persegi', 'inputs': ['Sisi (s)']},
            'rectangle': {'label': 'Persegi Panjang', 'inputs': ['Panjang (p)', 'Lebar (l)']},
            'circle': {'label': 'Lingkaran', 'inputs': ['Jari-jari (r)']},
            'triangle': {'label': 'Segitiga (Umum)', 'inputs': ['Alas (a)', 'Tinggi (t)', 'Sisi Miring/Lain (sm)']}, # Updated
            'trapezoid': {'label': 'Trapesium', 'inputs': ['Sisi Atas (a)', 'Sisi Bawah (b)', 'Tinggi (t)', 'Sisi Miring (sm)']}, # Updated
            'parallelogram': {'label': 'Jajar Genjang', 'inputs': ['Alas (a)', 'Tinggi (t)', 'Sisi Miring (sm)']}, # New
            'rhombus': {'label': 'Belah Ketupat', 'inputs': ['Diagonal 1 (d1)', 'Diagonal 2 (d2)', 'Sisi (s)']}, # New
            'kite': {'label': 'Layang-layang', 'inputs': ['Diagonal 1 (d1)', 'Diagonal 2 (d2)', 'Sisi Pendek (a)', 'Sisi Panjang (b)']} # New
        },
        'Bangun Ruang (3D)': {
            'cube': {'label': 'Kubus', 'inputs': ['Sisi (s)']},
            'block': {'label': 'Balok', 'inputs': ['Panjang (p)', 'Lebar (l)', 'Tinggi (t)']},
            'cylinder': {'label': 'Silinder / Tabung', 'inputs': ['Jari-jari (r)', 'Tinggi (t)']},
            'cone': {'label': 'Kerucut', 'inputs': ['Jari-jari (r)', 'Tinggi (t)']},
            'sphere': {'label': 'Bola', 'inputs': ['Jari-jari (r)']},
            'prism_tri': {'label': 'Prisma Segitiga Siku-siku', 'inputs': ['Alas Segitiga (a)', 'Tinggi Segitiga (ta)', 'Tinggi Prisma (t)']}, # New
            'pyramid': {'label': 'Limas Segiempat', 'inputs': ['Sisi Alas (s)', 'Tinggi Limas (t)']}
        }
    }

    # Default values
    s_cat = ''
    s_shape = ''
    inputs = {} 

    if request.method == 'POST':
        try:
            category = request.form.get('category')
            shape = request.form.get('shape')
            
            s_cat = category
            s_shape = shape
            
            # AMBIL SEMUA INPUT (Gunakan 0 jika kosong agar tidak error)
            def get_val(name): return float(request.form.get(name, 0) or 0)

            val_s = get_val('val_s') # Sisi
            val_p = get_val('val_p') # Panjang
            val_l = get_val('val_l') # Lebar
            val_t = get_val('val_t') # Tinggi (Umum)
            val_ta = get_val('val_ta') # Tinggi Alas (Prisma)
            val_r = get_val('val_r') # Jari-jari
            val_a = get_val('val_a') # Alas / Sisi Atas / Sisi Pendek
            val_b = get_val('val_b') # Sisi Bawah / Sisi Panjang
            val_sm = get_val('val_sm') # Sisi Miring
            val_d1 = get_val('val_d1') # Diagonal 1
            val_d2 = get_val('val_d2') # Diagonal 2

            # Simpan input user untuk dikembalikan ke form
            inputs = {
                's': request.form.get('val_s'), 'p': request.form.get('val_p'),
                'l': request.form.get('val_l'), 't': request.form.get('val_t'),
                'ta': request.form.get('val_ta'), 'r': request.form.get('val_r'),
                'a': request.form.get('val_a'), 'b': request.form.get('val_b'),
                'sm': request.form.get('val_sm'), 'd1': request.form.get('val_d1'),
                'd2': request.form.get('val_d2')
            }

            pi = 3.14159

            # --- LOGIKA 2D (LUAS & KELILING) ---
            if category == 'Bangun Datar (2D)':
                area = 0
                perimeter = 0
                
                if shape == 'square':
                    area = val_s ** 2
                    perimeter = 4 * val_s
                elif shape == 'rectangle':
                    area = val_p * val_l
                    perimeter = 2 * (val_p + val_l)
                elif shape == 'circle':
                    area = pi * (val_r ** 2)
                    perimeter = 2 * pi * val_r
                elif shape == 'triangle':
                    area = 0.5 * val_a * val_t
                    # Asumsi input Sisi Miring (sm) mewakili sisi lain untuk keliling sederhana
                    # Jika sm kosong, keliling estimasi
                    perimeter = val_a + val_t + val_sm if val_sm else "Butuh Sisi Miring"
                elif shape == 'parallelogram': # Jajar Genjang
                    area = val_a * val_t
                    perimeter = 2 * (val_a + val_sm)
                elif shape == 'trapezoid': # Trapesium
                    area = 0.5 * (val_a + val_b) * val_t
                    # Keliling asumsi trapesium sama kaki jika sm cuma 1
                    perimeter = val_a + val_b + (2 * val_sm)
                elif shape == 'rhombus': # Belah Ketupat
                    area = 0.5 * val_d1 * val_d2
                    perimeter = 4 * val_s
                elif shape == 'kite': # Layang-layang
                    area = 0.5 * val_d1 * val_d2
                    perimeter = 2 * (val_a + val_b)

                # Format Hasil
                res_kel = f"{perimeter:.2f}" if isinstance(perimeter, (int, float)) else perimeter
                result = f"Luas: {area:.2f} | Keliling: {res_kel}"

            # --- LOGIKA 3D (VOLUME & LUAS PERMUKAAN) ---
            elif category == 'Bangun Ruang (3D)':
                volume = 0
                surf_area = 0
                
                if shape == 'cube':
                    volume = val_s ** 3
                    surf_area = 6 * (val_s ** 2)
                elif shape == 'block':
                    volume = val_p * val_l * val_t
                    surf_area = 2 * ((val_p*val_l) + (val_p*val_t) + (val_l*val_t))
                elif shape == 'cylinder':
                    volume = pi * (val_r**2) * val_t
                    surf_area = 2 * pi * val_r * (val_r + val_t)
                elif shape == 'cone':
                    volume = (1/3) * pi * (val_r**2) * val_t
                    s = math.sqrt(val_r**2 + val_t**2) # Garis pelukis
                    surf_area = pi * val_r * (val_r + s)
                elif shape == 'sphere':
                    volume = (4/3) * pi * (val_r**3)
                    surf_area = 4 * pi * (val_r**2)
                elif shape == 'prism_tri': # Prisma Segitiga Siku-siku
                    # Alas segitiga siku-siku
                    area_base = 0.5 * val_a * val_ta
                    volume = area_base * val_t
                    # Keliling alas (Pythagoras untuk sisi miring segitiga)
                    hypotenuse = math.sqrt(val_a**2 + val_ta**2)
                    peri_base = val_a + val_ta + hypotenuse
                    surf_area = (2 * area_base) + (peri_base * val_t)
                elif shape == 'pyramid': # Limas Persegi
                    volume = (1/3) * (val_s**2) * val_t
                    t_segitiga = math.sqrt((val_s/2)**2 + val_t**2)
                    surf_area = (val_s**2) + (4 * 0.5 * val_s * t_segitiga)

                result = f"Volume: {volume:.2f} | Luas Permukaan: {surf_area:.2f}"

        except (ValueError, TypeError):
            result = "Error: Input tidak valid."

    return render_template('geometry.html', 
                           result=result, 
                           team=TEAM_INFO, 
                           geo_menu=GEO_MENU,
                           s_cat=s_cat, s_shape=s_shape, inputs=inputs)

# --- FITUR KONVERSI (DINAMIS) ---
@app.route('/conversion', methods=['GET', 'POST'])
def conversion():
    result = None
    input_val = ''
    cat_sel = ''
    from_sel = ''
    to_sel = ''

    if request.method == 'POST':
        try:
            category = request.form.get('category')
            val = float(request.form.get('value'))
            unit_from = request.form.get('unit_from')
            unit_to = request.form.get('unit_to')
            
            # Simpan pilihan user
            input_val = val
            cat_sel = category
            from_sel = unit_from
            to_sel = unit_to
            
            # LOGIKA SUHU
            if category == 'Suhu':
                c_val = 0
                # Ke Celcius
                if unit_from == 'Celcius (°C)': c_val = val
                elif unit_from == 'Fahrenheit (°F)': c_val = (val - 32) * 5/9
                elif unit_from == 'Kelvin (K)': c_val = val - 273.15
                elif unit_from == 'Reamur (°R)': c_val = val * 5/4
                
                # Dari Celcius ke Target
                res_val = 0
                if unit_to == 'Celcius (°C)': res_val = c_val
                elif unit_to == 'Fahrenheit (°F)': res_val = (c_val * 9/5) + 32
                elif unit_to == 'Kelvin (K)': res_val = c_val + 273.15
                elif unit_to == 'Reamur (°R)': res_val = c_val * 4/5
                
                result = f"{val} {unit_from} = {res_val:.2f} {unit_to}"

            # LOGIKA UMUM
            else:
                factor_from = UNIT_DATA[category][unit_from]
                factor_to = UNIT_DATA[category][unit_to]
                res_val = (val * factor_from) / factor_to
                
                # Format
                fmt_res = f"{int(res_val)}" if res_val.is_integer() else f"{res_val:.6g}"
                result = f"{val} {unit_from} = {fmt_res} {unit_to}"

        except (ValueError, KeyError, TypeError):
            result = "Error: Input tidak valid atau data tidak lengkap."

    return render_template('conversion.html', 
                           result=result, 
                           team=TEAM_INFO, 
                           unit_data=UNIT_DATA,
                           s_cat=cat_sel, s_from=from_sel, s_to=to_sel, s_val=input_val)

# --- FITUR MATERIAL (CALCULATOR BERAT LOGAM) ---
@app.route('/material', methods=['GET', 'POST'])
def material():
    result = None
    # Default values untuk form handling
    s_mat = ''
    s_shape = ''
    qty = 1
    dims = {} # Menyimpan input dimensi user

    if request.method == 'POST':
        try:
            # 1. Ambil Data Dasar
            mat_key = request.form.get('material')
            shape_key = request.form.get('shape')
            quantity = int(request.form.get('quantity'))
            
            # Simpan state untuk frontend
            s_mat = mat_key
            s_shape = shape_key
            qty = quantity

            # Ambil Density
            density = MATERIALS_DATA[mat_key]['density']
            mat_name = MATERIALS_DATA[mat_key]['name']

            # 2. Hitung Volume berdasarkan Bentuk
            # NOTE: Input user dalam milimeter (mm), kita ubah ke meter (m) -> bagi 1000
            volume_per_item = 0
            
            # Ambil input dimensi (gunakan 0 jika kosong agar tidak error)
            l = float(request.form.get('length', 0) or 0) / 1000      # Panjang
            w = float(request.form.get('width', 0) or 0) / 1000       # Lebar
            t = float(request.form.get('thickness', 0) or 0) / 1000   # Tebal
            od = float(request.form.get('outer_dia', 0) or 0) / 1000  # Diameter Luar
            id_val = float(request.form.get('inner_dia', 0) or 0) / 1000 # Diameter Dalam / ID
            
            # Simpan input mentah (mm) untuk dikembalikan ke form
            dims = {
                'l': request.form.get('length', ''),
                'w': request.form.get('width', ''),
                't': request.form.get('thickness', ''),
                'od': request.form.get('outer_dia', ''),
                'id': request.form.get('inner_dia', '')
            }

            # --- RUMUS VOLUME ---
            import math
            pi = 3.14159

            if shape_key == 'plate': # Plat Kotak (P x L x T)
                volume_per_item = l * w * t
                desc_shape = "Plat / Lembaran"

            elif shape_key == 'round_bar': # As Bulat Padat (Luas Alas x Panjang)
                radius = od / 2
                volume_per_item = pi * (radius ** 2) * l
                desc_shape = "Round Bar (As Bulat)"

            elif shape_key == 'square_bar': # As Kotak (Sisi x Sisi x Panjang)
                # Di sini Width dianggap sisi kotak
                volume_per_item = w * w * l
                desc_shape = "Square Bar (As Kotak)"

            elif shape_key == 'pipe': # Pipa / Tabung (Area Luar - Area Dalam) x Panjang
                r_out = od / 2
                # Jika user input tebal dinding (thickness), maka ID = OD - (2 x tebal)
                # Jika user input ID langsung, gunakan ID.
                # Kita prioritaskan Wall Thickness jika diisi.
                if t > 0:
                    r_in = r_out - t
                else:
                    r_in = id_val / 2
                
                area = pi * ((r_out**2) - (r_in**2))
                volume_per_item = area * l
                desc_shape = "Pipa / Tubing"

            # 3. Hitung Berat Total
            weight_per_item = volume_per_item * density
            total_weight = weight_per_item * quantity

            result = {
                'material': mat_name,
                'density': density,
                'shape': desc_shape,
                'qty': quantity,
                'weight_one': f"{weight_per_item:.3f}",
                'weight_total': f"{total_weight:.3f}"
            }

        except (ValueError, TypeError):
            result = "Error: Pastikan semua dimensi terisi angka dengan benar."

    return render_template('material.html', 
                           result=result, 
                           team=TEAM_INFO, 
                           materials=MATERIALS_DATA,
                           s_mat=s_mat, s_shape=s_shape, s_qty=qty, dims=dims)

# --- FITUR REKAYASA LANJUT (FLUID UPDATE) ---
@app.route('/engineering', methods=['GET', 'POST'])
def engineering():
    result = None
    active_tab = 'mech' 
    s_tool = ''
    inputs = {}
    
    # MATERIAL PROPERTIES (Structural - Tetap)
    MATERIALS_E = {
        'steel': {'name': 'Baja (Steel)', 'E': 200},
        'concrete': {'name': 'Beton (Concrete)', 'E': 25},
        'wood': {'name': 'Kayu (Wood)', 'E': 11},
        'alu': {'name': 'Aluminium', 'E': 69}
    }

    # 1. MEKANIKA (TETAP)
    MECH_MENU = {
        'lever': {'label': 'Tuas (Lever)', 'geo_inputs': ['Jarak Kuasa (d_in)', 'Jarak Beban (d_out)']},
        'pulley': {'label': 'Katrol (Pulley)', 'geo_inputs': ['Jumlah Tali (n)']},
        'screw': {'label': 'Sekrup (Screw)', 'geo_inputs': ['Jari-jari Putar (L)', 'Pitch Ulir (p)']},
        'wedge': {'label': 'Baji (Wedge)', 'geo_inputs': ['Panjang Sisi (L)', 'Tebal (t)']},
        'ramp': {'label': 'Bidang Miring', 'geo_inputs': ['Panjang (L)', 'Tinggi (h)']},
        'wheel': {'label': 'Roda Berporos', 'geo_inputs': ['Jari-jari Roda (R)', 'Jari-jari Poros (r)']}
    }

    # 2. STRUKTUR (TETAP)
    STRUCT_MENU = {
        'beam_simple': {'label': 'Balok Tumpuan Sederhana (Simply Supported)', 'type': 'beam'},
        'beam_cantilever': {'label': 'Balok Kantilever (Cantilever)', 'type': 'beam'},
        'stress_analysis': {'label': 'Cek Tegangan Material (Stress Check)', 'type': 'material'}
    }

    # 3. FLUIDA (UPDATED ala CALCTOOL)
    # Format: label, inputs (list label input)
    FLUID_MENU = {
        'flow_pipe': {
            'label': 'Debit Aliran Pipa (Pipe Flow Rate)',
            'inputs': ['Diameter Pipa (D) - mm', 'Kecepatan Aliran (v) - m/s']
        },
        'reynolds': {
            'label': 'Bilangan Reynolds (Reynolds Number)',
            'inputs': ['Massa Jenis (ρ) - kg/m³', 'Kecepatan (v) - m/s', 'Diameter Pipa (D) - mm', 'Viskositas Dinamis (μ) - Pa.s']
        },
        'hydrostatic': {
            'label': 'Tekanan Hidrostatis (Hydrostatic)',
            'inputs': ['Massa Jenis (ρ) - kg/m³', 'Kedalaman (h) - m', 'Gravitasi (g) - m/s²']
        },
        'bernoulli': {
            'label': 'Persamaan Bernoulli (Beda Tekanan)',
            'inputs': ['Massa Jenis (ρ) - kg/m³', 'Kecepatan 1 (v1) - m/s', 'Kecepatan 2 (v2) - m/s', 'Beda Ketinggian (h2-h1) - m']
        }
    }

    if request.method == 'POST':
        try:
            category = request.form.get('category')
            tool_type = request.form.get('tool_type')
            active_tab = category
            s_tool = tool_type
            inputs = request.form.to_dict() # Simpan input user

            def get_f(name): return float(request.form.get(name, 0) or 0)

            # --- LOGIKA 1: MECHANICAL (TETAP) ---
            if category == 'mech':
                # --- LOGIKA 1: MECHANICAL ADVANTAGE (UNIVERSAL) ---
            # Sesuai referensi: https://www.omnicalculator.com/physics/mechanical-advantage
                # Ambil 4 Variabel Utama
                f_load = get_f('f_load')    # Load Force (F_out)
                f_effort = get_f('f_effort') # Effort Force (F_in)
                d_input = get_f('d_input')   # Input Distance (d_in)
                d_output = get_f('d_output') # Output Distance (d_out)
                
                # Simpan input
                inputs = {'f_load': f_load, 'f_effort': f_effort, 'd_input': d_input, 'd_output': d_output}
                
                res_parts = []
                ama = 0
                ima = 0
                
                # 1. Hitung AMA (Actual Mechanical Advantage) = F_out / F_in
                if f_effort > 0:
                    ama = f_load / f_effort
                    res_parts.append(f"AMA (Aktual): {ama:.2f}x")
                
                # 2. Hitung IMA (Ideal Mechanical Advantage) = d_in / d_out
                if d_output > 0:
                    ima = d_input / d_output
                    res_parts.append(f"IMA (Ideal): {ima:.2f}x")
                
                # 3. Hitung Efisiensi = (AMA / IMA) * 100%
                if ima > 0 and ama > 0:
                    eff = (ama / ima) * 100
                    res_parts.append(f"Efisiensi: {eff:.2f}%")
                    
                    # Analisis Energi
                    w_in = f_effort * d_input
                    w_out = f_load * d_output
                    res_parts.append(f"Kerja (In): {w_in:.2f} J | Kerja (Out): {w_out:.2f} J")
                
                if not res_parts:
                    result = "Masukkan minimal data Gaya (untuk AMA) atau Jarak (untuk IMA)."
                else:
                    result = " | ".join(res_parts)
                pass 

            # --- LOGIKA 2: STRUCTURAL LOAD (UPDATED) ---
            elif category == 'struct':
                
                # A. ANALISIS BALOK (BEAM CALCULATOR)
                if 'beam' in tool_type:
                    # 1. Key Properties
                    L = get_f('length')     # Panjang (m)
                    b = get_f('width') / 1000 # mm ke m
                    h = get_f('height') / 1000 # mm ke m
                    mat_key = request.form.get('material')
                    
                    # 2. Load
                    load_val = get_f('load_val') # kN atau kN/m
                    load_type = request.form.get('load_type') # point / distributed

                    # Hitung Inersia (I) Persegi: b*h^3 / 12
                    I = (b * (h**3)) / 12
                    
                    # Ambil Modulus E (Konversi GPa ke kPa agar unit konsisten dengan kN)
                    E_gpa = MATERIALS_E[mat_key]['E']
                    E = E_gpa * 10**6 # kPa (kN/m²)

                    moment_max = 0
                    deflection_max = 0
                    shear_max = 0

                    # RUMUS BALOK SEDERHANA (Simply Supported)
                    if tool_type == 'beam_simple':
                        if load_type == 'point': # Beban Terpusat di Tengah
                            # M = P*L / 4
                            # Delta = P*L^3 / 48*E*I
                            moment_max = (load_val * L) / 4
                            deflection_max = (load_val * (L**3)) / (48 * E * I)
                            shear_max = load_val / 2
                        elif load_type == 'dist': # Beban Merata
                            # M = w*L^2 / 8
                            # Delta = 5*w*L^4 / 384*E*I
                            moment_max = (load_val * (L**2)) / 8
                            deflection_max = (5 * load_val * (L**4)) / (384 * E * I)
                            shear_max = (load_val * L) / 2

                    # RUMUS KANTILEVER (Cantilever)
                    elif tool_type == 'beam_cantilever':
                        if load_type == 'point': # Beban di Ujung
                            moment_max = load_val * L
                            deflection_max = (load_val * (L**3)) / (3 * E * I)
                            shear_max = load_val
                        elif load_type == 'dist': # Beban Merata
                            moment_max = (load_val * (L**2)) / 2
                            deflection_max = (load_val * (L**4)) / (8 * E * I)
                            shear_max = load_val * L

                    # Format Output
                    # Deflection ubah ke mm agar mudah dibaca
                    def_mm = deflection_max * 1000 
                    
                    result = {
                        'type': 'beam_res',
                        'I': f"{I:.2e} m⁴",
                        'M': f"{moment_max:.2f} kNm",
                        'V': f"{shear_max:.2f} kN",
                        'D': f"{def_mm:.2f} mm",
                        'desc': f"Analisis {STRUCT_MENU[tool_type]['label']} dengan material {MATERIALS_E[mat_key]['name']}"
                    }

                # B. ANALISIS MATERIAL (STRESS/STRAIN)
                elif tool_type == 'stress_analysis':
                    force = get_f('s_force')
                    area = get_f('s_area')
                    
                    stress = 0
                    if area > 0: stress = force / area
                    
                    result = f"Tegangan (Stress): {stress:.2f} N/mm² (MPa)"

            # --- LOGIKA 3: FLUIDA (UPDATED CALCTOOL STYLE) ---
            elif category == 'fluid':
                # Input Helper (v1..v4 sesuai urutan list inputs di menu)
                v1 = get_f('val1')
                v2 = get_f('val2')
                v3 = get_f('val3')
                v4 = get_f('val4')

                # 1. Flow Rate (Q = v * A)
                if tool_type == 'flow_pipe':
                    # v1: Diameter (mm) -> ubah ke meter
                    D = v1 / 1000
                    # v2: Velocity (m/s)
                    vel = v2
                    
                    area = math.pi * ((D / 2) ** 2)
                    Q = area * vel # m3/s
                    
                    # Konversi ke Liter/menit (LPM) umum di industri
                    Q_lpm = Q * 60000
                    
                    result = f"Debit Aliran (Q): {Q:.4f} m³/s  atau  {Q_lpm:.2f} Liter/menit"

                # 2. Reynolds Number (Re = rho * v * D / mu)
                elif tool_type == 'reynolds':
                    rho = v1
                    vel = v2
                    D = v3 / 1000 # mm ke m
                    mu = v4 # Dynamic Viscosity (Pa.s)
                    
                    if mu > 0:
                        Re = (rho * vel * D) / mu
                        
                        # Klasifikasi Aliran
                        status = "Transisi"
                        if Re < 2000: status = "Laminar (Halus)"
                        elif Re > 4000: status = "Turbulen (Kasar)"
                        
                        result = f"Reynolds Number (Re): {int(Re)} | Jenis Aliran: {status}"
                    else:
                        result = "Error: Viskositas tidak boleh nol."

                # 3. Hydrostatic Pressure (P = rho * g * h)
                elif tool_type == 'hydrostatic':
                    rho = v1
                    h = v2
                    g = v3 if v3 > 0 else 9.81 # Default g jika user isi 0
                    
                    P_pa = rho * g * h
                    P_bar = P_pa / 100000
                    
                    result = f"Tekanan: {P_pa:.2f} Pascal (Pa)  atau  {P_bar:.4f} Bar"

                # 4. Bernoulli (Pressure Difference)
                elif tool_type == 'bernoulli':
                    # Menghitung Delta P = 0.5 * rho * (v2^2 - v1^2) + rho * g * h
                    # Asumsi: Mencari P1 - P2
                    rho = v1
                    vel1 = v2
                    vel2 = v3
                    h_diff = v4 # h2 - h1
                    g = 9.81
                    
                    # Rumus Bernoulli: P1 + 0.5pv1^2 + pgh1 = P2 + 0.5pv2^2 + pgh2
                    # P1 - P2 = 0.5p(v2^2 - v1^2) + pg(h2 - h1)
                    
                    delta_P = (0.5 * rho * (vel2**2 - vel1**2)) + (rho * g * h_diff)
                    
                    result = f"Perbedaan Tekanan (ΔP): {delta_P:.2f} Pascal"

        except Exception as e:
            result = "Error: Pastikan input angka valid."

    return render_template('engineering.html', 
                           result=result, 
                           team=TEAM_INFO,
                           mech_menu=MECH_MENU, struct_menu=STRUCT_MENU, fluid_menu=FLUID_MENU,
                           materials=MATERIALS_E,
                           active_tab=active_tab, s_tool=s_tool, inputs=inputs)

# --- 4. MENJALANKAN APLIKASI (WAJIB DI BAWAH) ---
if __name__ == '__main__':
    app.run(debug=True)