import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.color import label2rgb
import pandas as pd
import os

# Change Z number to any slice you want
z_num = "Z0631"

c02_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}.tif"
c00_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif"
c01_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_{z_num}.tif"
mask_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}_cp_masks.tif"
csv_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif_results.csv"

# Paths
c02_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted", c02_file)
c00_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", c00_file)
c01_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C01_cropped", c01_file)
mask_path = os.path.join(r"D:\Conn_3dpipeline\masks", mask_file)
csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C00_synquant2", csv_file)

def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

# Crop coordinates
x, y, w, h = 6588, 252, 4992, 7740

# Load and process C02
c02 = tifffile.imread(c02_path)
c02_cropped = auto_contrast(c02[y:y+h, x:x+w])
c02_norm = c02_cropped / c02_cropped.max()

# Load mask and crop to same region
mask = tifffile.imread(mask_path)
mask_cropped = mask[y:y+h, x:x+w]

# Colored neuron overlay
neuron_overlay = label2rgb(mask_cropped, image=c02_norm, bg_label=0, alpha=0.4)
neuron_count = len(np.unique(mask_cropped)) - 1

# Load C00 and synaptic dots
c00 = tifffile.imread(c00_path)
c00_display = auto_contrast(c00)
c00_norm = c00_display / c00_display.max()

df_synapses = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame(columns=['X','Y'])

# Load C01
c01_exists = os.path.exists(c01_path)
if c01_exists:
    c01 = tifffile.imread(c01_path)
    c01_display = auto_contrast(c01)
    c01_norm = c01_display / c01_display.max()

# Plot
fig, axes = plt.subplots(1, 4, figsize=(40, 10))

# Panel 1 â€” C02 with neuron overlay
axes[0].imshow(neuron_overlay)
axes[0].set_title(f'C02 - Neurons ({neuron_count})')
axes[0].axis('off')

# Panel 2 â€” C00 with GlyT2 dots
axes[1].imshow(c00_norm, cmap='gray')
axes[1].scatter(df_synapses['X'], df_synapses['Y'], 
                c='yellow', s=3, alpha=0.6, label=f'GlyT2 dots ({len(df_synapses)})')
axes[1].set_title(f'C00 - GlyT2 Dots ({len(df_synapses)})')
axes[1].legend(loc='upper right', fontsize=8)
axes[1].axis('off')

# Panel 3 â€” C01 if available
if c01_exists:
    axes[2].imshow(c01_norm, cmap='gray')
    axes[2].set_title('C01 - Gephyrin')
    axes[2].axis('off')
else:
    axes[2].text(0.5, 0.5, 'C01 not available', 
                ha='center', va='center', transform=axes[2].transAxes)
    axes[2].axis('off')

# Panel 4 â€” Combined overlay
axes[3].imshow(c00_norm, cmap='gray')
axes[3].imshow(mask_cropped > 0, alpha=0.2, cmap='Reds')
axes[3].scatter(df_synapses['X'], df_synapses['Y'],
                c='yellow', s=3, alpha=0.6)
axes[3].set_title('Combined - Neurons + GlyT2 Dots')
axes[3].axis('off')

plt.suptitle(f'Slice {z_num} - TDP-43', fontsize=16)
plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\full_overlay.png", dpi=150)
plt.show()
print("Saved full_overlay.png")