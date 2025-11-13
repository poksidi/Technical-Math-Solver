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
        info: 'Satuan panjang digunakan untuk mengukur jarak atau dimensi benda. Meter (m) adalah satuan dasar dalam Sistem Internasional (SI).'
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
        info: 'Satuan massa digunakan untuk mengukur berat atau jumlah materi. Kilogram (kg) adalah satuan dasar dalam Sistem Internasional (SI).'
    },
    temperature: {
        units: {
            'c': 'Celcius',
            'f': 'Fahrenheit',
            'k': 'Kelvin'
        },
        info: 'Satuan suhu digunakan untuk mengukur tingkat panas atau dingin. Celcius umum digunakan sehari-hari, Kelvin untuk keperluan ilmiah.'
    }
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeUnitConverter();
    loadCalculationHistory();
    loadRecentConversions();
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
            const fromOption = new Option(`${label} (${value})`, value);
            const toOption = new Option(`${label} (${value})`, value);
            fromUnitSelect.add(fromOption);
            toUnitSelect.add(toOption);
        });
        
        // Set different default to-unit for better UX
        if (category === 'length') {
            toUnitSelect.value = 'cm';
        } else if (category === 'mass') {
            toUnitSelect.value = 'g';
        } else if (category === 'temperature') {
            toUnitSelect.value = 'f';
        }
        
        // Update unit info
        if (unitInfo) {
            unitInfo.innerHTML = `
                <h6 class="fw-bold text-primary">${category.charAt(0).toUpperCase() + category.slice(1)}</h6>
                <p class="mb-3">${unitData[category].info}</p>
                <div class="mt-3">
                    <h6 class="fw-semibold mb-2">Satuan Tersedia:</h6>
                    <div class="d-flex flex-wrap gap-2">
                        ${Object.entries(units).map(([value, label]) => 
                            `<span class="badge bg-primary">${label} (${value})</span>`
                        ).join('')}
                    </div>
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
            const category = this.dataset.category;
            const fromUnit = this.dataset.from;
            const toUnit = this.dataset.to;
            
            // Set the form values
            document.getElementById('category').value = category;
            
            // Trigger change event to update units
            document.getElementById('category').dispatchEvent(new Event('change'));
            
            // Small delay to ensure units are populated
            setTimeout(() => {
                document.getElementById('from-unit').value = fromUnit;
                document.getElementById('to-unit').value = toUnit;
                
                // Show prompt for value
                const fromLabel = unitData[category].units[fromUnit];
                const value = prompt(`Masukkan nilai dalam ${fromLabel} (${fromUnit}):`);
                if (value !== null && !isNaN(parseFloat(value))) {
                    document.getElementById('value').value = parseFloat(value);
                    handleUnitConversion(new Event('submit'));
                }
            }, 100);
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
    
    hideError();
    
    const valueInput = document.getElementById('value');
    const value = parseFloat(valueInput.value);
    
    if (isNaN(value)) {
        showError('Masukkan nilai yang valid');
        return;
    }
    
    const formData = {
        value: value,
        from_unit: document.getElementById('from-unit').value,
        to_unit: document.getElementById('to-unit').value,
        category: document.getElementById('category').value
    };
    
    try {
        // Show loading state
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Mengkonversi...';
        submitBtn.disabled = true;
        
        const response = await fetch('/api/convert-units', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        // Restore button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        if (data.success) {
            const resultDiv = document.getElementById('conversion-result');
            const resultText = document.getElementById('result-text');
            
            const fromLabel = unitData[formData.category].units[formData.from_unit];
            const toLabel = unitData[formData.category].units[formData.to_unit];
            
            resultText.innerHTML = `
                <span class="text-primary">${formData.value} ${fromLabel} (${formData.from_unit})</span>
                <br>
                <span class="fs-4">=</span>
                <br>
                <span class="text-success">${data.formatted_result} ${toLabel} (${formData.to_unit})</span>
            `;
            
            resultDiv.style.display = 'block';
            resultDiv.className = 'mt-4 fade-in';
            
            // Show success animation
            showSuccessAnimation();
            
            // Reload history and recent conversions
            loadCalculationHistory();
            loadRecentConversions();
        } else {
            showError(data.error || 'Terjadi kesalahan saat melakukan konversi');
        }
    } catch (error) {
        const submitBtn = e.target.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Konversi Sekarang';
        submitBtn.disabled = false;
        
        showError('Terjadi kesalahan jaringan. Periksa koneksi internet Anda.');
    }
}

// Load recent conversions
async function loadRecentConversions() {
    try {
        const response = await fetch('/api/history');
        const history = await response.json();
        
        const recentContainer = document.getElementById('recent-conversions');
        if (recentContainer) {
            const conversions = history.filter(item => item.type === 'unit_conversion').slice(0, 5);
            
            if (conversions.length === 0) {
                recentContainer.innerHTML = '<p class="text-muted mb-0">Belum ada konversi terbaru.</p>';
                return;
            }
            
            let html = '';
            conversions.forEach(calc => {
                html += `
                    <div class="border-start border-primary ps-2 mb-2">
                        <div class="fw-semibold">${calc.input} → ${calc.output}</div>
                        <small class="text-muted">${new Date(calc.timestamp).toLocaleTimeString('id-ID')}</small>
                    </div>
                `;
            });
            
            recentContainer.innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading recent conversions:', error);
    }
}

// Error handling functions
function showError(message) {
    hideError();
    const errorDiv = document.getElementById('conversion-error');
    const errorMessage = document.getElementById('error-message');
    
    if (errorDiv && errorMessage) {
        errorMessage.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.classList.add('fade-in');
    }
}

function hideError() {
    const errorDiv = document.getElementById('conversion-error');
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
}

// ... (fungsi lainnya tetap sama, pastikan semua menggunakan try-catch) ...

// Enhanced result display with confetti effect
function showSuccessAnimation() {
    // Simple confetti effect
    const confettiCount = 20;
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
        confetti.style.width = '8px';
        confetti.style.height = '8px';
        confetti.style.background = getRandomColor();
        confetti.style.borderRadius = '50%';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.top = '-10px';
        confetti.style.animation = `confettiFall ${Math.random() * 1.5 + 0.5}s ease-in forwards`;
        confetti.style.animationDelay = Math.random() * 0.5 + 's';
        
        container.appendChild(confetti);
    }
    
    document.body.appendChild(container);
    
    // Remove confetti after animation
    setTimeout(() => {
        if (document.body.contains(container)) {
            document.body.removeChild(container);
        }
    }, 2000);
}

function getRandomColor() {
    const colors = ['#6366f1', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444', '#3b82f6'];
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
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Modern animations and interactions
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

// Initialize when page loads
window.addEventListener('load', function() {
    initializeAnimations();
    initScrollAnimations();
});
