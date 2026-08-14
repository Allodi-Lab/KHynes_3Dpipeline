import tifffile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure
import os

# Change this to any slice you want to check
filename = "14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_Z0631.tif"
image_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", filename)
csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C00_synquant2", filename + "_results.csv")

# Load image
img = tifffile.imread(image_path)

# Auto contrast
p2, p98 = np.percentile(img, (2, 98))
img_display = exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

# Load results
df = pd.read_csv(csv_path)
print(f"Detected {len(df)} synaptic dots")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

# Original with auto contrast
axes[0].imshow(img_display, cmap='gray')
axes[0].set_title('Original Image (Auto Contrast)')
axes[0].axis('off')

# Image with detections
axes[1].imshow(img_display, cmap='gray')
axes[1].scatter(df['X'], df['Y'], c='yellow', s=5, alpha=0.7)
axes[1].set_title(f'Detected Synaptic Dots: {len(df)}')
axes[1].axis('off')

plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\detection_visualization.png", dpi=150)
plt.show()
print("Saved visualization to results folder")