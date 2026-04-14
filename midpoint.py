import matplotlib.pyplot as plt

def draw_circle_points(xc, yc, x, y):
    """Fungsi untuk menghasilkan 8 titik simetris lingkaran."""
    return [
        (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
    ]

def midpoint_circle(xc, yc, r):
    """Implementasi algoritma Midpoint untuk membentuk lingkaran."""
    x = 0
    y = r
    # Parameter keputusan awal
    p = 1 - r
    
    all_points = []
    # Tambahkan titik awal di 8 oktan
    all_points.extend(draw_circle_points(xc, yc, x, y))
    
    while x < y:
        x += 1
        if p < 0:
            # Titik berikutnya adalah (x+1, y)
            p = p + 2 * x + 1
        else:
            # Titik berikutnya adalah (x+1, y-1)
            y -= 1
            p = p + 2 * x - 2 * y + 1
        
        all_points.extend(draw_circle_points(xc, yc, x, y))
    
    return all_points

# --- Bagian Input Dinamis ---
try:
    print("=== Implementasi Algoritma Midpoint Circle ===")
    pusat_x = int(input("Masukkan koordinat X pusat: "))
    pusat_y = int(input("Masukkan koordinat Y pusat: "))
    radius = int(input("Masukkan nilai radius (r): "))

    # Eksekusi algoritma
    points = midpoint_circle(pusat_x, pusat_y, radius)

    # --- Visualisasi Menggunakan Matplotlib ---
    x_coords, y_coords = zip(*points)
    
    plt.figure(figsize=(7, 7))
    plt.scatter(x_coords, y_coords, color='blue', s=20, label='Titik Lingkaran')
    plt.plot(pusat_x, pusat_y, 'ro', label='Pusat (xc, yc)') # Titik pusat
    
    plt.title(f"Lingkaran Midpoint (Pusat: {pusat_x},{pusat_y}, Radius: {radius})")
    plt.xlabel("Sumbu X")
    plt.ylabel("Sumbu Y")
    plt.gca().set_aspect('equal', adjustable='box') # Memastikan lingkaran tidak lonjong
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

except ValueError:
    print("Mohon masukkan angka bulat (integer) yang valid.")