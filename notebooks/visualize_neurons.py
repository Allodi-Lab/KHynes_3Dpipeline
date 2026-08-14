import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.color import label2rgb
import os

# Change Z number to any slice you want
filename = "14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_Z0631.tif"
mask_filename = filename.replace('.tif', '_cp_masks.tif')

image_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted", filename)
mask_path = os.path.join(r"D:\Conn_3dpipeline\masks", mask_filename)

img = tifffile.imread(image_path)
mask = tifffile.imread(mask_path)

# Auto contrast
p2, p98 = np.percentile(img, (2, 98))
img_display = exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

# Normalize to 0-1 for label2rgb
img_normalized = img_display / img_display.max()

# Create colored overlay — each neuron gets a different color
overlay = label2rgb(mask, image=img_normalized, bg_label=0, alpha=0.4)

neuron_count = len(np.unique(mask)) - 1  # subtract background
print(f"Found {neuron_count} neurons")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(20, 10))

axes[0].imshow(img_normalized, cmap='gray')
axes[0].set_title('Original C02 Image')
axes[0].axis('off')

axes[1].imshow(overlay)
axes[1].set_title(f'Segmented Neurons: {neuron_count}')
axes[1].axis('off')

plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\neuron_visualization.png", dpi=150)
plt.show()
print("Saved")

axes[1].imshow(img_display, cmap='gray')
axes[1].imshow(mask, alpha=0.3, cmap='jet')
axes[1].scatter(centroids_x, centroids_y, c='red', s=50, marker='x')
axes[1].set_title(f'Segmented Neurons: {len(neuron_ids)}')
axes[1].axis('off')

plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\neuron_visualization.png", dpi=150)
plt.show()
print("Saved")
