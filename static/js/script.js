// Unit conversion data
const unitData = {
    length: {
        units: {
            'mm': 'Milimeter',
            'cm': 'Centimeter', 
            'm': 'Meter',
            'km': 'Kilometer',
            'in': 'Inchi',
            'ft': 'Kaki',
            'yd': 'Yard',
            'mi': 'Mil'
        },
        info: 'Satuan panjang digunakan untuk mengukur jarak atau dimensi benda.'
    },
    mass: {
        units: {
            'mg': 'Miligram',
            'g': 'Gram',
            'kg': 'Kilogram', 
            'ton': 'Ton',
            'oz': 'Ons',
            'lb': 'Pound'
        },
        info: 'Satuan massa digunakan untuk mengukur berat atau jumlah materi.'
    },
    temperature: {
        units: {
            'c': 'Celcius',
            'f': 'Fahrenheit',
            'k': 'Kelvin'
        },
        info: 'Satuan suhu digunakan untuk mengukur tingkat panas atau dingin.'
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeUnitConverter();
    loadCalculationHistory();
    setupEventListeners();
});

function initializeUnitConverter() {
    const categorySelect = document.getElementById('category');
    const fromUnitSelect = document.getElementById('from-unit');
    const toUnitSelect = document.getElementById('to-unit');
    const unitInfo = document.getElementById('unit-info');
    
    if (categorySelect) {
        // Populate initial units
        updateUnitOptions(categorySelect.value);
        
        categorySelect.addEventListener('change', function() {
            updateUnitOptions(this.value);
        });
    }
    
    function updateUnitOptions(category) {
        const units = unitData[category].units;
        
        // Clear existing options
        fromUnitSelect.innerHTML = '';
        toUnitSelect.innerHTML = '';
        
        // Add new options
        Object.entries(units).forEach(([value, label]) => {
            const fromOption = new Option(label, value);
            const toOption = new Option(label, value);
            fromUnitSelect.add(fromOption);
            toUnitSelect.add(toOption);
        });
        
        // Update unit info
        if (unitInfo) {
            unitInfo.innerHTML = `
                <h6>${category.charAt(0).toUpperCase() + category.slice(1)}</h6>
                <p class="mb-2">${unitData[category].info}</p>
                <div class="mt-3">
                    ${Object.entries(units).map(([value, label]) => 
                        `<span class="unit-badge me-2 mb-2 d-inline-block">${label} (${value})</span>`
                    ).join('')}
                </div>
            `;
        }
    }
}

// Setup event listeners for all pages
function setupEventListeners() {
    // Unit conversion form
    const conversionForm = document.getElementById('conversion-form');
    if (conversionForm) {
        conversionForm.addEventListener('submit', handleUnitConversion);
    }
    
    // Quick conversion buttons
    document.querySelectorAll('.quick-convert').forEach(button => {
        button.addEventListener('click', function() {
            const fromUnit = this.dataset.from;
            const toUnit = this.dataset.to;
            
            // Set the form values
            document.getElementById('from-unit').value = fromUnit;
            document.getElementById('to-unit').value = toUnit;
            
            // Show prompt for value
            const value = prompt(`Masukkan nilai dalam ${fromUnit}:`);
            if (value !== null && !isNaN(value)) {
                document.getElementById('value').value = value;
                handleUnitConversion(new Event('submit'));
            }
        });
    });
    
    // Electrical calculations
    const electricalForm = document.getElementById('electrical-form');
    if (electricalForm) {
        electricalForm.addEventListener('submit', handleElectricalCalculation);
    }
    
    // Material calculations
    const materialForm = document.getElementById('material-form');
    if (materialForm) {
        materialForm.addEventListener('submit', handleMaterialCalculation);
    }
    
    // Geometry calculations
    const geometryForm = document.getElementById('geometry-form');
    if (geometryForm) {
        geometryForm.addEventListener('submit', handleGeometryCalculation);
    }
}

// Handle unit conversion
async function handleUnitConversion(e) {
    e.preventDefault();
    
    const formData = {
        value: document.getElementById('value').value,
        from_unit: document.getElementById('from-unit').value,
        to_unit: document.getElementById('to-unit').value,
        category: document.getElementById('category').value
    };
    
    try {
        const response = await fetch('/api/convert-units', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            const resultDiv = document.getElementById('conversion-result');
            const resultText = document.getElementById('result-text');
            
            resultText.textContent = 
                `${formData.value} ${formData.from_unit} = ${data.result} ${formData.to_unit}`;
            resultDiv.style.display = 'block';
            resultDiv.className = 'mt-3 alert alert-success fade-in';
            
            // Reload history
            loadCalculationHistory();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Terjadi kesalahan saat melakukan konversi');
    }
}

// Handle electrical calculations
async function handleElectricalCalculation(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        type: formData.get('calculation-type')
    };
    
    // Collect relevant inputs based on calculation type
    if (data.type === 'ohms_law') {
        if (formData.get('voltage')) data.voltage = parseFloat(formData.get('voltage'));
        if (formData.get('current')) data.current = parseFloat(formData.get('current'));
        if (formData.get('resistance')) data.resistance = parseFloat(formData.get('resistance'));
    } else if (data.type === 'series_parallel') {
        data.circuit_type = formData.get('circuit-type');
        data.resistors = formData.get('resistors').split(',').map(r => parseFloat(r.trim()));
    }
    
    try {
        const response = await fetch('/api/electrical-calc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayElectricalResult(result.result, data.type);
            loadCalculationHistory();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Terjadi kesalahan saat melakukan perhitungan');
    }
}

// Handle material calculations
async function handleMaterialCalculation(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        type: formData.get('calculation-type')
    };
    
    if (data.type === 'volume_weight') {
        data.length = parseFloat(formData.get('length'));
        data.width = parseFloat(formData.get('width'));
        data.height = parseFloat(formData.get('height'));
        data.density = parseFloat(formData.get('density'));
    } else if (data.type === 'beam_stress') {
        data.load = parseFloat(formData.get('load'));
        data.length = parseFloat(formData.get('beam-length'));
        data.width = parseFloat(formData.get('beam-width'));
        data.height = parseFloat(formData.get('beam-height'));
    }
    
    try {
        const response = await fetch('/api/material-calc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayMaterialResult(result.result, data.type);
            loadCalculationHistory();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Terjadi kesalahan saat melakukan perhitungan');
    }
}

// Handle geometry calculations
async function handleGeometryCalculation(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {
        shape: formData.get('shape')
    };
    
    // Collect shape-specific inputs
    if (data.shape === 'rectangle') {
        data.length = parseFloat(formData.get('rect-length'));
        data.width = parseFloat(formData.get('rect-width'));
    } else if (data.shape === 'circle') {
        data.radius = parseFloat(formData.get('circle-radius'));
    } else if (data.shape === 'triangle') {
        data.base = parseFloat(formData.get('triangle-base'));
        data.height = parseFloat(formData.get('triangle-height'));
        data.side1 = parseFloat(formData.get('triangle-side1'));
        data.side2 = parseFloat(formData.get('triangle-side2'));
    } else if (data.shape === 'cylinder') {
        data.radius = parseFloat(formData.get('cylinder-radius'));
        data.height = parseFloat(formData.get('cylinder-height'));
    }
    
    try {
        const response = await fetch('/api/geometry-calc', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayGeometryResult(result.result, data.shape);
            loadCalculationHistory();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Terjadi kesalahan saat melakukan perhitungan');
    }
}

// Display functions for different calculation types
function displayElectricalResult(result, type) {
    const resultDiv = document.getElementById('electrical-result');
    let html = '<h5>Hasil Perhitungan:</h5><div class="result-highlight">';
    
    if (type === 'ohms_law') {
        Object.entries(result).forEach(([key, value]) => {
            const label = {
                'voltage': 'Tegangan',
                'current': 'Arus', 
                'resistance': 'Hambatan',
                'power': 'Daya'
            }[key] || key;
            const unit = {
                'voltage': 'V',
                'current': 'A',
                'resistance': 'Ω', 
                'power': 'W'
            }[key] || '';
            
            html += `<p><strong>${label}:</strong> ${value} ${unit}</p>`;
        });
    } else if (type === 'series_parallel') {
        html += `<p><strong>Hambatan Total:</strong> ${result.total_resistance} Ω</p>`;
    }
    
    html += '</div>';
    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';
}

function displayMaterialResult(result, type) {
    const resultDiv = document.getElementById('material-result');
    let html = '<h5>Hasil Perhitungan:</h5><div class="result-highlight">';
    
    if (type === 'volume_weight') {
        html += `
            <p><strong>Volume:</strong> ${result.volume} m³</p>
            <p><strong>Berat:</strong> ${result.weight} kg</p>
        `;
    } else if (type === 'beam_stress') {
        html += `
            <p><strong>Tegangan:</strong> ${result.stress} Pa</p>
            <p><strong>Luas Penampang:</strong> ${result.area} m²</p>
        `;
    }
    
    html += '</div>';
    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';
}

function displayGeometryResult(result, shape) {
    const resultDiv = document.getElementById('geometry-result');
    let html = '<h5>Hasil Perhitungan:</h5><div class="result-highlight">';
    
    Object.entries(result).forEach(([key, value]) => {
        const label = {
            'area': 'Luas',
            'perimeter': 'Keliling',
            'circumference': 'Keliling',
            'volume': 'Volume',
            'surface_area': 'Luas Permukaan'
        }[key] || key;
        
        const unit = key.includes('area') || key.includes('volume') ? 'satuan²' : 'satuan';
        
        html += `<p><strong>${label}:</strong> ${value} ${unit}</p>`;
    });
    
    html += '</div>';
    resultDiv.innerHTML = html;
    resultDiv.style.display = 'block';
}

// Load calculation history
async function loadCalculationHistory() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();
        
        const historyContainer = document.getElementById('calculation-history');
        if (historyContainer) {
            if (history.length === 0) {
                historyContainer.innerHTML = '<p class="text-muted">Belum ada riwayat perhitungan.</p>';
                return;
            }
            
            let html = `
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Waktu</th>
                            <th>Jenis</th>
                            <th>Input</th>
                            <th>Output</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            history.reverse().forEach(calc => {
                const time = new Date(calc.timestamp).toLocaleString('id-ID');
                const typeLabel = {
                    'unit_conversion': 'Konversi Satuan',
                    'electrical_ohms_law': 'Hukum Ohm',
                    'electrical_circuit': 'Rangkaian Listrik',
                    'material_volume_weight': 'Volume & Berat',
                    'material_beam_stress': 'Tegangan Balok',
                    'geometry_rectangle': 'Persegi Panjang',
                    'geometry_circle': 'Lingkaran',
                    'geometry_triangle': 'Segitiga',
                    'geometry_cylinder': 'Silinder'
                }[calc.type] || calc.type;
                
                let inputText = typeof calc.input === 'object' ? 
                    JSON.stringify(calc.input).substring(0, 50) + '...' : 
                    calc.input;
                
                let outputText = typeof calc.output === 'object' ?
                    JSON.stringify(calc.output) : calc.output;
                
                html += `
                    <tr>
                        <td>${time}</td>
                        <td>${typeLabel}</td>
                        <td>${inputText}</td>
                        <td>${outputText}</td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            historyContainer.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Utility function to show errors
function showError(message) {
    // Create or update error alert
    let errorAlert = document.getElementById('error-alert');
    if (!errorAlert) {
        errorAlert = document.createElement('div');
        errorAlert.id = 'error-alert';
        errorAlert.className = 'alert alert-danger alert-dismissible fade show';
        errorAlert.innerHTML = `
            <span id="error-message"></span>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('main').prepend(errorAlert);
    }
    
    document.getElementById('error-message').textContent = message;
    errorAlert.style.display = 'block';
}

// Export function for global access
window.TechnicalMathSolver = {
    convertUnits: handleUnitConversion,
    calculateElectrical: handleElectricalCalculation,
    calculateMaterial: handleMaterialCalculation,
    calculateGeometry: handleGeometryCalculation
};

// Modern animations and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations
    initializeAnimations();
    
    // Add intersection observer for scroll animations
    initScrollAnimations();
});

function initializeAnimations() {
    // Add loading animation to cards
    const cards = document.querySelectorAll('.card, .feature-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all cards and sections
    const elementsToAnimate = document.querySelectorAll('.card, .feature-card, .glass-card');
    elementsToAnimate.forEach(el => {
        observer.observe(el);
    });
}

// Enhanced result display with confetti effect
function showSuccessAnimation() {
    // Simple confetti effect
    const confettiCount = 30;
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '100%';
    container.style.height = '100%';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '9999';
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.background = getRandomColor();
        confetti.style.borderRadius = '50%';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = '-10px';
        confetti.style.animation = `confettiFall ${Math.random() * 2 + 1}s ease-in forwards`;
        
        container.appendChild(confetti);
    }
    
    document.body.appendChild(container);
    
    // Remove confetti after animation
    setTimeout(() => {
        document.body.removeChild(container);
    }, 2000);
}

function getRandomColor() {
    const colors = [
        '#6366f1', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Add CSS for confetti animation
const style = document.createElement('style');
style.textContent = `
    @keyframes confettiFall {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);