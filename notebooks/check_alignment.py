import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
import os

# Use same Z number for both
z_num = "Z0631"

c02_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_Z0631.tif"
c00_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_Z0631.tif"

c02_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted", c02_file)
c00_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", c00_file)

# Load both
c02 = tifffile.imread(c02_path)
c00 = tifffile.imread(c00_path)

# Auto contrast both
def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

c02_display = auto_contrast(c02)
c00_display = auto_contrast(c00)

# Crop C02 to same region as C00
x, y, w, h = 6588, 252, 4992, 7740
c02_cropped = c02_display[y:y+h, x:x+w]

print(f"C02 full size: {c02.shape}")
print(f"C00 cropped size: {c00.shape}")
print(f"C02 cropped size: {c02_cropped.shape}")

# Plot all three
fig, axes = plt.subplots(1, 3, figsize=(30, 10))

axes[0].imshow(c02_display, cmap='gray')
axes[0].set_title('C02 Full Image')
axes[0].axis('off')

axes[1].imshow(c02_cropped, cmap='gray')
axes[1].set_title('C02 Cropped to same region as C00')
axes[1].axis('off')

axes[2].imshow(c00_display, cmap='gray')
axes[2].set_title('C00 Cropped Image')
axes[2].axis('off')

plt.tight_layout()
plt.savefig(r"D:\Conn_3dpipeline\results\alignment_check.png", dpi=100)
plt.show()
print("Saved alignment_check.png")