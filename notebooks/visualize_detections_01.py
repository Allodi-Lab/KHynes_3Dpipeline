import tifffile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure
import os

# Change Z number to any slice you want
filename = "14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_Z0631.tif"

image_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C01_cropped", filename)
csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C01_synquant", filename + "_results.csv")

# Load image
img = tifffile.imread(image_path)

# Auto contrast
p2, p98 = np.percentile(img, (2, 98))
img_display = exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))
img_norm = img_display / img_display.max()

# Load results
df = pd.read_csv(csv_path)
print(f"Detected {len(df)} Gephyrin synaptic dots")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Original with auto contrast
axes[0].imshow(img_norm, cmap='gray')
axes[0].set_title('C01 — Gephyrin Channel (Auto Contrast)')
axes[0].axis('off')

# Image with detections
axes[1].imshow(img_norm, cmap='gray')
axes[1].scatter(df['X'], df['Y'], c='cyan', s=5, alpha=0.7)
axes[1].set_title(f'Detected Gephyrin Dots: {len(df)}')
axes[1].axis('off')

plt.suptitle(f'C01 Gephyrin Detection — Z0631', fontsize=14)
plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\C01_detection_visualization.png", dpi=150)
plt.show()
print("Saved C01_detection_visualization.png")

# LEFT PANEL — shows the raw C01 Gephyrin channel image with auto contrast applied,
# making the postsynaptic structures visible. Gephyrin marks the receiving side of
# glycinergic synapses on motor neurons.

# RIGHT PANEL — shows the same image with detected Gephyrin synaptic dots overlaid
# in cyan. Each dot represents one detected postsynaptic site. Compare with the
# C00 GlyT2 visualization (yellow dots) to see pre and postsynaptic coverage.