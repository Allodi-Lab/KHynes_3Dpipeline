import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.color import label2rgb
import pandas as pd
import os

z_num = "Z0631"

c00_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif"
mask_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}_cp_masks.tif"
csv_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif_results.csv"

c00_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", c00_file)
mask_path = os.path.join(r"D:\Conn_3dpipeline\masks", mask_file)
csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C00_synquant2", csv_file)
results_path = r"D:\Conn_3dpipeline\results\matching\TDP43_synapse_counts.csv"

def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

x, y, w, h = 6588, 252, 4992, 7740

# Load images
c00 = tifffile.imread(c00_path)
c00_norm = auto_contrast(c00)
c00_norm = c00_norm / c00_norm.max()

mask = tifffile.imread(mask_path)
mask_cropped = mask[y:y+h, x:x+w]

# Load synapse dots
df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame(columns=['X','Y'])

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

print(f"Neurons in slice: {len(neuron_ids)}")
print(f"Total matched synapses: {sum(synapse_counts)}")
print(f"Mean synapses per neuron: {sum(synapse_counts)/len(synapse_counts) if synapse_counts else 0:.2f}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(24, 12))

# Left â€” all dots and neuron centres
axes[0].imshow(c00_norm, cmap='gray')
axes[0].scatter(df['X'], df['Y'], c='yellow', s=3, alpha=0.5, label=f'GlyT2 dots ({len(df)})')
if len(centroids_x) > 0:
    axes[0].scatter(centroids_x, centroids_y, c='red', s=100, 
                   marker='o', alpha=0.8, label=f'Neurons ({len(neuron_ids)})')
axes[0].set_title(f'All Detections - Z{z_num}', fontsize=14)
axes[0].legend(fontsize=10)
axes[0].axis('off')

# Right â€” neurons coloured by synapse count
axes[1].imshow(c00_norm, cmap='gray')
axes[1].imshow(mask_cropped > 0, alpha=0.15, cmap='Reds')
if len(centroids_x) > 0:
    sc = axes[1].scatter(centroids_x, centroids_y, c=synapse_counts,
                        s=300, cmap='cool', alpha=0.9, zorder=5,
                        vmin=0, vmax=max(synapse_counts) if synapse_counts else 1)
    plt.colorbar(sc, ax=axes[1], label='GlyT2 synapse count')
axes[1].set_title(f'Neurons Coloured by Synapse Count - Z{z_num}', fontsize=14)
axes[1].axis('off')

plt.suptitle(f'Matching Results - TDP-43 Slice {z_num}', fontsize=16)
plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\matching_visualization.png", dpi=150)
plt.show()
print("Saved matching_visualization.png")

# LEFT PANEL: shows all detected GlyT2 synaptic dots (yellow) with red circles
# marking the centre of each segmented neuron. Use this to check that dots and
# neurons are spatially aligned correctly.

# RIGHT PANEL: shows each neuron coloured by how many GlyT2 synaptic dots were
# matched to it. Blue = few synapses, pink = many synapses. This is the core
# result of the pipeline.