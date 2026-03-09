import pandas as pd
import matplotlib.pyplot as plt

# 1. Membaca Database
df = pd.read_csv("tips.csv")

# 2. Menyiapkan Data untuk Plot 1 (Gender)
gender_counts = df['sex'].value_counts()
gender_labels = gender_counts.index
gender_sizes = gender_counts.values

# 3. Menyiapkan Data untuk Plot 2 (Rata-rata Tips per Hari)
rata_tips_hari = df.groupby('day')['tip'].mean().sort_values()
hari_labels = rata_tips_hari.index
tips_values = rata_tips_hari.values

# 4. Membuat Figure dengan 2 Subplot (1 baris, 2 kolom)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Dashboard Analisis Tips Restoran', fontsize=20, weight='bold', y=1.05)

# --- PLOT 1: DONUT CHART (KIRI) ---
colors_gender = ['#3366CC', '#DC3912']
explode = (0.05, 0)
ax1.pie(gender_sizes, explode=explode, labels=gender_labels, colors=colors_gender,
        autopct='%1.1f%%', shadow=True, startangle=140, pctdistance=0.85,
        textprops={'fontsize': 12, 'weight': 'bold'})


centre_circle = plt.Circle((0,0), 0.70, fc='white')
ax1.add_artist(centre_circle)
ax1.set_title("Proporsi Pemberi Tips (Gender)", fontsize=14, pad=15)
ax1.text(0, 0, f"Total\n{gender_sizes.sum()}", ha='center', va='center', fontsize=12, weight='bold')

# --- PLOT 2: HORIZONTAL BAR CHART (KANAN) ---
colors_day = ['#FFC300', '#FF5733', '#C70039', '#900C3F']
bars = ax2.barh(hari_labels, tips_values, color=colors_day, height=0.6)


for bar in bars:
    width = bar.get_width()
    ax2.text(width + 0.02, bar.get_y() + bar.get_height()/2, 
             f'${width:.2f}', va='center', fontsize=11, fontweight='bold')

ax2.set_title("Rata-rata Tips per Hari", fontsize=14, pad=15)
ax2.set_xlabel("Besar Tips (USD)")
ax2.grid(axis='x', linestyle='--', alpha=0.6)


ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()