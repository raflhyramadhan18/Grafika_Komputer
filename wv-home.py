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

# Definisi Batas 
window_bounds = (20, 80, 40, 80)
# Kita coba kembalikan ke ukuran viewport awal agar tidak distorsi parah
viewport_bounds = (30, 60, 40, 60) 

# ================= MENDATA OBJEK (RUMAH) =================
# Kita pisahkan bagian rumah agar plot-nya tidak menyambung semua menjadi satu garis berantakan

dinding_window_x = [35, 65, 65, 35, 35]
dinding_window_y = [40, 40, 60, 60, 40]

atap_window_x = [35, 50, 65]
atap_window_y = [60, 75, 60]

pintu_window_x = [45, 55, 55, 45, 45]
pintu_window_y = [40, 40, 50, 50, 40]

# List untuk menampung seluruh bagian rumah
objek_window = [
    (dinding_window_x, dinding_window_y),
    (atap_window_x, atap_window_y),
    (pintu_window_x, pintu_window_y)
]

# List untuk menampung hasil transformasi Viewport
objek_viewport = []

# ================= PROSES TRANSFORMASI =================

# Looping untuk setiap bagian rumah (dinding, atap, pintu)
for bagian_x, bagian_y in objek_window:
    hasil_x = []
    hasil_y = []
    # Looping untuk setiap titik dalam satu bagian
    for i in range(len(bagian_x)):
        xv, yv = window_to_viewport(
            bagian_x[i], 
            bagian_y[i], 
            window_bounds, 
            viewport_bounds
        )
        hasil_x.append(xv)
        hasil_y.append(yv)
    
    objek_viewport.append((hasil_x, hasil_y))

# ================= VISUALISASI =================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# --- Plot 1: Window ---
# Menggambar setiap bagian rumah
for i, (x_vals, y_vals) in enumerate(objek_window):
    label_nama = "Rumah" if i == 0 else "" # Hanya beri label di dinding agar legend tidak penuh
    ax1.plot(x_vals, y_vals, marker='o', color='blue', label=label_nama)

ax1.set_xlim(0, 100) 
ax1.set_ylim(0, 100)
window_rect = plt.Rectangle((window_bounds[0], window_bounds[2]), 
                            window_bounds[1]-window_bounds[0], 
                            window_bounds[3]-window_bounds[2], 
                            fill=False, edgecolor='red', linestyle='--')
ax1.add_patch(window_rect)
ax1.set_title('World Coordinate (Window)')
ax1.grid(True)
ax1.legend(['Objek Asli', 'Batas Window'])


# --- Plot 2: Viewport ---
# Menggambar setiap bagian rumah hasil transformasi
for i, (x_vals, y_vals) in enumerate(objek_viewport):
    label_nama = "Rumah di Viewport" if i == 0 else "" 
    ax2.plot(x_vals, y_vals, marker='o', color='green', label=label_nama)

ax2.set_xlim(0, 100)
ax2.set_ylim(0, 100)
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