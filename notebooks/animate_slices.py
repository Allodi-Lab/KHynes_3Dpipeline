import tifffile
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage import exposure
from skimage.color import label2rgb
import pandas as pd
import os

# Folders
masks_folder = r"D:\Conn_3dpipeline\masks"
c00_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"
synquant_folder = r"D:\Conn_3dpipeline\results\C00_synquant2"
output_path = r"D:\Conn_3dpipeline\results\TDP43_slice_animation.gif"

# Crop offset
x_off, y_off = 6588, 252

def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

# Get all mask files in Z order
mask_files = sorted([f for f in os.listdir(masks_folder) if f.endswith('_cp_masks.tif')])

# Only use every 10th slice to keep gif manageable
mask_files = mask_files[::10]
print(f"Animating {len(mask_files)} slices")

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
plt.suptitle('TDP-43 — Synaptic Connections Through Spinal Cord Depth', fontsize=14)

frames = []

for mask_filename in mask_files:
    z_num = mask_filename.split('_Z')[-1].replace('_cp_masks.tif', '')
    
    # Build C00 filename
    c00_filename = mask_filename.replace('_C02_', '_C00_').replace('_cp_masks.tif', '.tif')
    c00_path = os.path.join(c00_folder, c00_filename)
    mask_path = os.path.join(masks_folder, mask_filename)
    csv_filename = c00_filename + '_results.csv'
    csv_path = os.path.join(synquant_folder, csv_filename)
    
    if not os.path.exists(c00_path) or not os.path.exists(mask_path):
        continue
    
    # Load images
    c00 = tifffile.imread(c00_path)
    c00_norm = auto_contrast(c00)
    c00_norm = c00_norm / c00_norm.max()
    
    mask = tifffile.imread(mask_path)
    x, y, w, h = 6588, 252, 4992, 7740
    mask_cropped = mask[y:y+h, x:x+w]
    
    # Neuron overlay
    overlay = label2rgb(mask_cropped, image=c00_norm, bg_label=0, alpha=0.35)
    neuron_count = len(np.unique(mask_cropped)) - 1
    
    # Load synaptic dots
    dot_x, dot_y = [], []
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if len(df) > 0:
            dot_x = df['X'].values
            dot_y = df['Y'].values
    
    # Build frame
    im1 = axes[0].imshow(overlay, animated=True)
    axes[0].set_title(f'Neurons — Z{z_num} ({neuron_count} detected)', fontsize=10)
    axes[0].axis('off')
    
    im2 = axes[1].imshow(c00_norm, cmap='gray', animated=True)
    axes[1].set_title(f'GlyT2 Synaptic Dots — Z{z_num} ({len(dot_x)} detected)', fontsize=10)
    axes[1].axis('off')
    
    sc = None
    if len(dot_x) > 0:
        sc = axes[1].scatter(dot_x, dot_y, c='yellow', s=3, alpha=0.6, animated=True)
    
    frame_artists = [im1, im2]
    if sc is not None:
        frame_artists.append(sc)
    
    frames.append(frame_artists)
    print(f"Built frame for Z{z_num} — {len(dot_x)} dots, {neuron_count} neurons")

print("Saving animation — this may take a few minutes...")
ani = animation.ArtistAnimation(fig, frames, interval=200, blit=True, repeat_delay=1000)
ani.save(output_path, writer='pillow', fps=5)
plt.close()
print(f"Saved to {output_path}")