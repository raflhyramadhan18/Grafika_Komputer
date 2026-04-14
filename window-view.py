import matplotlib.pyplot as plt

def window_to_viewport(x_w, y_w, window, viewport):
    """
    Fungsi untuk mentransformasikan titik dari Window ke Viewport.
    """
    xw_min, xw_max, yw_min, yw_max = window
    xv_min, xv_max, yv_min, yv_max = viewport

    # 1. Menghitung Scaling Factor (Sx dan Sy)
    sx = (xv_max - xv_min) / (xw_max - xw_min)
    sy = (yv_max - yv_min) / (yw_max - yw_min)

    # 2. Menghitung koordinat baru di Viewport
    x_v = xv_min + (x_w - xw_min) * sx
    y_v = yv_min + (y_w - yw_min) * sy

    return x_v, y_v

# ================= KONDISI AWAL =================

# Definisi Batas (xmin, xmax, ymin, ymax)
# Kita ambil contoh angka dari materi slide
window_bounds = (20, 80, 40, 80)
viewport_bounds = (30, 60, 40, 60)

# Objek yang akan digambar (Misal: Sebuah Segitiga)
# Titik A(30, 45), B(50, 75), C(70, 45), kembali ke A(30,45) agar garis tertutup
objek_window_x = [30, 50, 70, 30]
objek_window_y = [45, 75, 45, 45]

# Array untuk menampung titik hasil transformasi
objek_viewport_x = []
objek_viewport_y = []

# ================= PROSES TRANSFORMASI =================

# Melakukan perulangan untuk setiap titik pada objek
for i in range(len(objek_window_x)):
    xv, yv = window_to_viewport(
        objek_window_x[i], 
        objek_window_y[i], 
        window_bounds, 
        viewport_bounds
    )
    objek_viewport_x.append(xv)
    objek_viewport_y.append(yv)

# ================= VISUALISASI =================

# Membuat figure dengan 2 subplot (kiri dan kanan)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Plot 1: Window
ax1.plot(objek_window_x, objek_window_y, marker='o', color='blue', label='Objek')
ax1.set_xlim(0, 100) # Memperluas area grafik agar kotak window terlihat
ax1.set_ylim(0, 100)
# Menggambar kotak Window
window_rect = plt.Rectangle((window_bounds[0], window_bounds[2]), 
                            window_bounds[1]-window_bounds[0], 
                            window_bounds[3]-window_bounds[2], 
                            fill=False, edgecolor='red', linestyle='--')
ax1.add_patch(window_rect)
ax1.set_title('World Coordinate (Window)')
ax1.grid(True)
ax1.legend(['Objek Asli', 'Batas Window'])

# Plot 2: Viewport
ax2.plot(objek_viewport_x, objek_viewport_y, marker='o', color='green', label='Objek Ter-map')
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
# Menggambar kotak Viewport
viewport_rect = plt.Rectangle((viewport_bounds[0], viewport_bounds[2]), 
                                viewport_bounds[1]-viewport_bounds[0], 
                                viewport_bounds[3]-viewport_bounds[2], 
                                fill=False, edgecolor='purple', linestyle='--')
ax2.add_patch(viewport_rect)
ax2.set_title('Device Coordinate (Viewport)')
ax2.grid(True)
ax2.legend(['Objek di Viewport', 'Batas Viewport'])

plt.tight_layout()
plt.show()