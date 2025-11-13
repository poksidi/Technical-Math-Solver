import qrcode
import json
from PIL import Image

# Data identitas kelompok sesuai template
team_data = {
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

# Convert data to JSON string
json_data = json.dumps(team_data, indent=2)

# Create QR code instance
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Add data to QR code
qr.add_data(json_data)
qr.make(fit=True)

# Create QR code image
img = qr.make_image(fill_color="black", back_color="white")

# Save QR code
img.save("static/images/qr-code.png")

print("QR Code berhasil dibuat: static/images/qr-code.png")
print("Data yang di-encode:")
print(json_data)