/* SMART DRAWING LOGIC (VECTOR-BASED: MOVE & EDIT) */

const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");
const paperArea = document.getElementById("paperArea");

// --- STATE MANAGEMENT ---
let shapes = [];        // Menyimpan semua objek gambar {type, x, y, w, h, color, size, ...}
let currentShape = null; // Objek yang sedang digambar saat drag
let isDrawing = false;
let selectedTool = "select"; // Default tool
let startX, startY;

// Variabel untuk Move/Select
let selectedShapeIndex = -1;
let isDraggingShape = false;
let dragOffsetX, dragOffsetY;

// Settings Elements
const colorPicker = document.getElementById("strokeColor");
const widthPicker = document.getElementById("lineWidth");

// --- 1. SETUP CANVAS ---
window.addEventListener("load", () => {
    canvas.width = 820;
    canvas.height = 574;
    if(paperArea) paperArea.classList.add('show-grid');
    redrawCanvas(); // Init
});

// --- 2. TOOL SELECTION ---
function setTool(tool) {
    selectedTool = tool;
    selectedShapeIndex = -1; // Reset seleksi saat ganti alat
    redrawCanvas();

    // Update UI Buttons
    document.querySelectorAll(".tool-btn").forEach(btn => btn.classList.remove("active", "btn-primary", "text-white"));
    document.querySelectorAll(".tool-btn").forEach(btn => btn.classList.add("btn-white"));
    
    const activeBtn = document.querySelector(`button[onclick="setTool('${tool}')"]`);
    if(activeBtn) {
        activeBtn.classList.remove("btn-white");
        activeBtn.classList.add("btn-primary", "text-white", "active");
    }
    
    // Ubah cursor sesuai tool
    canvas.style.cursor = (tool === 'select') ? 'default' : 'crosshair';
}

// --- 3. CORE EVENT LISTENERS ---

const getPos = (e) => {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
};

// MOUSEDOWN
canvas.addEventListener("mousedown", (e) => {
    const { x, y } = getPos(e);
    startX = x;
    startY = y;

    // A. LOGIKA SELECT / MOVE
    if (selectedTool === 'select') {
        // Cek apakah klik mengenai suatu objek (dari yang paling baru/atas)
        selectedShapeIndex = -1;
        for (let i = shapes.length - 1; i >= 0; i--) {
            if (isHit(shapes[i], x, y)) {
                selectedShapeIndex = i;
                isDraggingShape = true;
                // Hitung selisih posisi mouse dengan pojok objek agar gesernya mulus
                dragOffsetX = x - shapes[i].x;
                dragOffsetY = y - shapes[i].y;
                redrawCanvas();
                return;
            }
        }
        // Jika klik di ruang kosong, deselect
        redrawCanvas();
    }
    // B. LOGIKA TEXT (Langsung ketik)
    else if (selectedTool === 'text') {
        addText(x, y);
    }
    // C. LOGIKA GAMBAR BARU
    else {
        isDrawing = true;
        // Buat template objek sementara
        currentShape = {
            type: selectedTool,
            x: startX, y: startY, w: 0, h: 0, // w & h akan diupdate saat drag
            color: colorPicker.value,
            size: widthPicker.value,
            points: (selectedTool === 'brush' || selectedTool === 'eraser') ? [{x, y}] : null // Khusus brush
        };
    }
});

// MOUSEMOVE
canvas.addEventListener("mousemove", (e) => {
    const { x, y } = getPos(e);

    // A. MOVE OBJECT
    if (selectedTool === 'select' && isDraggingShape && selectedShapeIndex !== -1) {
        const s = shapes[selectedShapeIndex];
        
        // Update posisi objek
        if (s.type === 'brush' || s.type === 'eraser') {
            // Khusus brush, kita geser seluruh titiknya
            const dx = x - startX; 
            const dy = y - startY;
            s.points.forEach(p => { p.x += dx; p.y += dy; });
            startX = x; startY = y; // Reset start untuk delta berikutnya
        } else {
            // Shape biasa (Line, Rect, Building, dll)
            s.x = x - dragOffsetX;
            s.y = y - dragOffsetY;
        }
        redrawCanvas();
    }
    // B. DRAWING NEW OBJECT
    else if (isDrawing && currentShape) {
        if (currentShape.type === 'brush' || currentShape.type === 'eraser') {
            currentShape.points.push({x, y});
        } else {
            // Update dimensi shape berdasarkan drag
            currentShape.w = x - startX;
            currentShape.h = y - startY;
        }
        redrawCanvas();
    }
});

// MOUSEUP
const endAction = () => {
    if (isDrawing && currentShape) {
        // Simpan objek permanen ke array
        // Cegah objek ukuran 0 (klik doang)
        if (Math.abs(currentShape.w) > 2 || Math.abs(currentShape.h) > 2 || currentShape.points) {
            shapes.push(currentShape);
        }
    }
    isDrawing = false;
    currentShape = null;
    isDraggingShape = false;
    redrawCanvas();
};

canvas.addEventListener("mouseup", endAction);
canvas.addEventListener("mouseleave", endAction);


// --- 4. REDRAW SYSTEM (INTI DARI VECTOR MODE) ---
function redrawCanvas() {
    // 1. Bersihkan Canvas Total
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 2. Gambar Ulang Semua Shape dari History
    shapes.forEach(shape => drawShapeObject(shape));

    // 3. Gambar Shape yang sedang dibuat (Preview)
    if (isDrawing && currentShape) {
        drawShapeObject(currentShape);
    }

    // 4. Highlight Seleksi (Jika ada yang dipilih)
    if (selectedShapeIndex !== -1 && selectedTool === 'select') {
        const s = shapes[selectedShapeIndex];
        ctx.strokeStyle = '#00f'; // Warna biru seleksi
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]); // Garis putus-putus
        
        if (s.type === 'brush' || s.type === 'eraser') {
            // Kotak seleksi untuk brush agak tricky, kita skip dulu biar simpel
        } else {
            // Gambar kotak pembantu di sekeliling objek
            // Normalisasi koordinat untuk kotak seleksi
            let bx = s.x, by = s.y, bw = s.w, bh = s.h;
            if (s.type === 'line') { bw = s.w; bh = s.h; } 
            
            ctx.strokeRect(bx - 5, by - 5, bw + 10, bh + 10);
        }
        ctx.setLineDash([]); // Reset
    }
}

// --- 5. SHAPE RENDERER ---
function drawShapeObject(s) {
    ctx.beginPath();
    ctx.lineWidth = s.size;
    ctx.strokeStyle = s.type === 'eraser' ? '#fff' : s.color; // Eraser jadi warna putih (karena background putih)
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Jika eraser, tebalkan sedikit
    if (s.type === 'eraser') ctx.lineWidth = s.size * 5;

    // --- BRUSH / FREEHAND ---
    if (s.type === 'brush' || s.type === 'eraser') {
        if (s.points.length < 2) return;
        ctx.moveTo(s.points[0].x, s.points[0].y);
        for (let i = 1; i < s.points.length; i++) {
            ctx.lineTo(s.points[i].x, s.points[i].y);
        }
        ctx.stroke();
        return;
    }

    // --- STANDARD & BUILDING SHAPES ---
    // Gunakan fungsi pembantu, tapi passing parameternya adalah properti objek
    // Kita sesuaikan agar fungsi drawHelper menggunakan x, y, w, h
    const x = s.x;
    const y = s.y;
    const w = s.w;
    const h = s.h;

    if (s.type === 'line') {
        ctx.moveTo(x, y);
        ctx.lineTo(x + w, y + h);
        ctx.stroke();
    } else if (s.type === 'rect') {
        ctx.strokeRect(x, y, w, h);
    } else if (s.type === 'circle') {
        let r = Math.sqrt(w*w + h*h);
        ctx.arc(x, y, r, 0, 2 * Math.PI);
        ctx.stroke();
    } else if (s.type === 'text') {
        ctx.font = "bold " + (parseInt(s.size) * 3 + 10) + "px Arial";
        ctx.fillStyle = s.color;
        ctx.fillText(s.text, x, y);
    } 
    // MAPPING FUNGSI HELPER
    else if (s.type === 'room_l') drawLShapePath(ctx, x, y, w, h);
    else if (s.type === 'room_t') drawTShapePath(ctx, x, y, w, h);
    else if (s.type === 'room_u') drawUShapePath(ctx, x, y, w, h);
    else if (s.type === 'room_plus') drawPlusShapePath(ctx, x, y, w, h);
    else if (s.type === 'door_single') drawDoorSinglePath(ctx, x, y, w, h);
    else if (s.type === 'door_double') drawDoorDoublePath(ctx, x, y, w, h);
    else if (s.type === 'window_fix') drawWindowFixPath(ctx, x, y, w, h);
    else if (s.type === 'window_slide') drawWindowSlidePath(ctx, x, y, w, h);
}

// --- 6. HIT DETECTION (Untuk Klik Select) ---
function isHit(s, mx, my) {
    if (s.type === 'brush' || s.type === 'eraser') {
        // Cek jarak mouse ke setiap titik brush (agak berat tapi akurat)
        return s.points.some(p => Math.hypot(p.x - mx, p.y - my) < 10);
    }
    
    // Bounding Box Logic sederhana
    // Normalisasi w dan h (karena bisa negatif jika drag ke kiri/atas)
    let rx = s.x, ry = s.y, rw = s.w, rh = s.h;
    if (rw < 0) { rx += rw; rw = -rw; }
    if (rh < 0) { ry += rh; rh = -rh; }

    return (mx >= rx && mx <= rx + rw && my >= ry && my <= ry + rh);
}

// --- 7. HELPER PATH FUNCTIONS (Refactored for Redraw) ---
// Fungsi ini hanya membuat path, tidak ada beginPath() di dalamnya agar fleksibel

function drawLShapePath(c, x, y, w, h) {
    const thX = w/3, thY = h/3;
    c.beginPath(); c.moveTo(x, y); c.lineTo(x, y+h); c.lineTo(x+w, y+h);
    c.lineTo(x+w, y+h-thY); c.lineTo(x+thX, y+h-thY); c.lineTo(x+thX, y);
    c.closePath(); c.stroke();
}
function drawTShapePath(c, x, y, w, h) {
    const thX = w/3, thY = h/3;
    c.beginPath(); c.moveTo(x, y); c.lineTo(x+w, y); c.lineTo(x+w, y+thY);
    c.lineTo(x+(w/2)+(thX/2), y+thY); c.lineTo(x+(w/2)+(thX/2), y+h);
    c.lineTo(x+(w/2)-(thX/2), y+h); c.lineTo(x+(w/2)-(thX/2), y+thY); c.lineTo(x, y+thY);
    c.closePath(); c.stroke();
}
function drawUShapePath(c, x, y, w, h) {
    const thX = w/4, thY = h/3;
    c.beginPath(); c.moveTo(x, y); c.lineTo(x, y+h); c.lineTo(x+w, y+h);
    c.lineTo(x+w, y); c.lineTo(x+w-thX, y); c.lineTo(x+w-thX, y+h-thY);
    c.lineTo(x+thX, y+h-thY); c.lineTo(x+thX, y);
    c.closePath(); c.stroke();
}
function drawPlusShapePath(c, x, y, w, h) {
    const pX = w/3, pY = h/3;
    c.beginPath(); c.moveTo(x+pX, y); c.lineTo(x+pX*2, y); c.lineTo(x+pX*2, y+pY);
    c.lineTo(x+w, y+pY); c.lineTo(x+w, y+pY*2); c.lineTo(x+pX*2, y+pY*2);
    c.lineTo(x+pX*2, y+h); c.lineTo(x+pX, y+h); c.lineTo(x+pX, y+pY*2);
    c.lineTo(x, y+pY*2); c.lineTo(x, y+pY); c.lineTo(x+pX, y+pY);
    c.closePath(); c.stroke();
}
// DOORS & WINDOWS
function drawDoorSinglePath(c, x, y, w, h) {
    const radius = Math.sqrt(w*w + h*h); // Approximate for visual
    c.beginPath(); c.moveTo(x, y); c.lineTo(x+w, y); // Daun
    c.moveTo(x, y); c.lineTo(x, y+h); // Kusen
    c.stroke();
    // Arc (Simplified)
    c.beginPath(); c.moveTo(x+w, y); c.quadraticCurveTo(x+w, y+h, x, y+h); c.stroke();
}
function drawDoorDoublePath(c, x, y, w, h) {
    const midX = x + w/2;
    c.strokeRect(x, y, w, h); // Frame
    c.beginPath(); c.moveTo(midX, y); c.lineTo(midX, y+h); c.stroke(); // Center
}
function drawWindowFixPath(c, x, y, w, h) {
    c.strokeRect(x, y, w, h);
    c.beginPath(); c.moveTo(x, y+h/2); c.lineTo(x+w, y+h/2); c.stroke();
}
function drawWindowSlidePath(c, x, y, w, h) {
    c.strokeRect(x, y, w, h);
    c.beginPath(); c.moveTo(x+w/2, y); c.lineTo(x+w/2, y+h); c.stroke();
}

// --- UTILITIES (TEXT, CLEAR, DL) ---
function addText(x, y) {
    let text = prompt("Masukkan Label:", "");
    if (text) {
        shapes.push({
            type: 'text', text: text, x: x, y: y, 
            color: colorPicker.value, size: widthPicker.value
        });
        redrawCanvas();
    }
}

function clearCanvas() {
    shapes = []; // Hapus history
    redrawCanvas();
}

function toggleGrid() { if (paperArea) paperArea.classList.toggle('show-grid'); }

function downloadCanvas(el) {
    // Render final ke canvas temporary putih
    let tempCanvas = document.createElement('canvas');
    let tCtx = tempCanvas.getContext('2d');
    tempCanvas.width = canvas.width; tempCanvas.height = canvas.height;
    tCtx.fillStyle = "#ffffff"; tCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // Draw all shapes to temp canvas
    // Kita perlu sedikit modifikasi drawShapeObject agar bisa menerima context (c) yang berbeda
    // Tapi cara cepat: render main canvas (karena transparan) di atas putih
    tCtx.drawImage(canvas, 0, 0);

    // Draw Etiket (Title Block) - SAMA SEPERTI SEBELUMNYA
    // ... [Paste kode Draw Etiket dari jawaban sebelumnya di sini jika ingin etiket] ...
    // Untuk ringkasnya, kita download raw canvas dulu
    
    const imageURI = tempCanvas.toDataURL("image/png");
    let link = document.createElement('a'); link.download = "design.png"; link.href = imageURI;
    document.body.appendChild(link); link.click(); document.body.removeChild(link);
}