## FIRST FILE 
import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.color import label2rgb
import pandas as pd
import os

z_num = "Z0631"

c00_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif"
c01_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_{z_num}.tif"
mask_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}_cp_masks.tif"
c00_csv = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif_results.csv"
c01_csv = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_{z_num}.tif_results.csv"

c00_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", c00_file)
c01_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C01_cropped", c01_file)
mask_path = os.path.join(r"D:\Conn_3dpipeline\masks", mask_file)
c00_csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C00_synquant2", c00_csv)
c01_csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C01_synquant", c01_csv)
results_path = r"D:\Conn_3dpipeline\results\matching\TDP43_synapse_counts.csv"

def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

x, y, w, h = 6588, 252, 4992, 7740

# Load all images
c00 = tifffile.imread(c00_path)
c00_norm = auto_contrast(c00)
c00_norm = c00_norm / c00_norm.max()

c01 = tifffile.imread(c01_path)
c01_norm = auto_contrast(c01)
c01_norm = c01_norm / c01_norm.max()

mask = tifffile.imread(mask_path)
mask_cropped = mask[y:y+h, x:x+w]

# Colored neuron overlay
overlay = label2rgb(mask_cropped, image=c00_norm, bg_label=0, alpha=0.35)
neuron_count = len(np.unique(mask_cropped)) - 1

# Load synapse dots
df_c00 = pd.read_csv(c00_csv_path) if os.path.exists(c00_csv_path) else pd.DataFrame(columns=['X','Y'])
df_c01 = pd.read_csv(c01_csv_path) if os.path.exists(c01_csv_path) else pd.DataFrame(columns=['X','Y'])

# Load matching results
results_df = pd.read_csv(results_path)
z_stripped = z_num.replace('Z', '').lstrip('0') or '0'
slice_results = results_df[results_df['Z_slice'].astype(str).str.lstrip('0') == z_stripped]

# Get neuron centroids and synapse counts
neuron_ids = np.unique(mask_cropped)
neuron_ids = neuron_ids[neuron_ids > 0]
centroids_x, centroids_y, synapse_counts = [], [], []

for nid in neuron_ids:
    positions = np.where(mask_cropped == nid)
    centroids_y.append(np.mean(positions[0]))
    centroids_x.append(np.mean(positions[1]))
    count = slice_results[slice_results['neuron_id'] == nid]['GlyT2_synapse_count'].values
    synapse_counts.append(count[0] if len(count) > 0 else 0)

# Plot - 2 rows, 3 columns
fig, axes = plt.subplots(2, 3, figsize=(36, 20))
plt.suptitle(f'TDP-43 Full Pipeline - Slice {z_num}', fontsize=18)

# Row 1
# Panel 1 - C00 GlyT2 channel
axes[0, 0].imshow(c00_norm, cmap='gray')
axes[0, 0].set_title(f'C00 â€” GlyT2 Channel', fontsize=12)
axes[0, 0].axis('off')

# Panel 2 - C01 Gephyrin channel
axes[0, 1].imshow(c01_norm, cmap='gray')
axes[0, 1].set_title(f'C01 â€” Gephyrin Channel', fontsize=12)
axes[0, 1].axis('off')

# Panel 3 - Neurons colored overlay
axes[0, 2].imshow(overlay)
axes[0, 2].set_title(f'C02 â€” Neurons ({neuron_count} detected)', fontsize=12)
axes[0, 2].axis('off')

# Row 2
# Panel 4 â€” C00 with GlyT2 dots
axes[1, 0].imshow(c00_norm, cmap='gray')
axes[1, 0].scatter(df_c00['X'], df_c00['Y'], c='yellow', s=3, alpha=0.6)
axes[1, 0].set_title(f'GlyT2 Dots ({len(df_c00)} detected)', fontsize=12)
axes[1, 0].axis('off')

# Panel 5 - C01 with Gephyrin dots
axes[1, 1].imshow(c01_norm, cmap='gray')
axes[1, 1].scatter(df_c01['X'], df_c01['Y'], c='cyan', s=3, alpha=0.6)
axes[1, 1].set_title(f'Gephyrin Dots ({len(df_c01)} detected)', fontsize=12)
axes[1, 1].axis('off')

# Panel 6 - Combined all together
axes[1, 2].imshow(c00_norm, cmap='gray')
axes[1, 2].imshow(mask_cropped > 0, alpha=0.15, cmap='Reds')
axes[1, 2].scatter(df_c00['X'], df_c00['Y'], c='yellow', s=2, alpha=0.5, label='GlyT2')
axes[1, 2].scatter(df_c01['X'], df_c01['Y'], c='cyan', s=2, alpha=0.5, label='Gephyrin')
if len(centroids_x) > 0:
    sc = axes[1, 2].scatter(centroids_x, centroids_y, c=synapse_counts,
                            s=150, cmap='cool', alpha=0.9, zorder=5)
    plt.colorbar(sc, ax=axes[1, 2], label='GlyT2 synapse count')
axes[1, 2].legend(fontsize=8, loc='upper right')
axes[1, 2].set_title('Combined - All Channels + Matching', fontsize=12)
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\full_pipeline_visualization.png", dpi=150)
plt.show()
print("Saved full_pipeline_visualization.png")