import tifffile
import numpy as np
import vedo
from skimage import exposure
import os

print("Loading images...")

# Load a few representative slices for 3D rendering
masks_folder = r"D:\Conn_3dpipeline\masks"
c00_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"

# Use every 20th slice
mask_files = sorted([f for f in os.listdir(masks_folder) 
                     if f.endswith('_cp_masks.tif')])[::20]

print(f"Loading {len(mask_files)} slices...")

c00_stack = []
mask_stack = []

x, y, w, h = 6588, 252, 4992, 7740

for f in mask_files:
    # Load mask
    mask = tifffile.imread(os.path.join(masks_folder, f))
    mask_cropped = mask[y:y+h, x:x+w]
    mask_stack.append(mask_cropped)
    
    # Load matching C00
    c00_file = f.replace('_C02_', '_C00_').replace('_cp_masks.tif', '.tif')
    c00_path = os.path.join(c00_folder, c00_file)
    if os.path.exists(c00_path):
        c00 = tifffile.imread(c00_path)
        p2, p98 = np.percentile(c00, (2, 98))
        c00_norm = exposure.rescale_intensity(c00.astype(float), in_range=(p2, p98))
        c00_norm = (c00_norm / c00_norm.max() * 255).astype(np.uint8)
        c00_stack.append(c00_norm)
    else:
        c00_stack.append(np.zeros((h, w), dtype=np.uint8))

c00_volume = np.stack(c00_stack, axis=0)
mask_volume = np.stack(mask_stack, axis=0)

print(f"Volume shape: {c00_volume.shape}")

# Create vedo volume
print("Creating 3D rendering...")
vol = vedo.Volume(c00_volume, spacing=(20, 1, 1))
vol.color(['black', 'blue', 'cyan', 'white'])
vol.alpha([0, 0.1, 0.3, 0.8])

# Add neuron surfaces
plotter = vedo.Plotter(offscreen=True, size=(1000, 1000))

frames = []
for angle in range(0, 360, 5):
    plotter.clear()
    plotter.add(vol)
    plotter.camera.SetPosition(500, 500, 500)
    plotter.show(azimuth=angle)
    frame = plotter.screenshot(asarray=True)
    frames.append(frame)
    print(f"Frame {angle//5 + 1}/72")

import imageio
imageio.mimsave(r"D:\Conn_3dpipeline\results\neurons_3d_volume.gif",
                frames, fps=10)
print("Done. Saved neurons_3d_volume.gif")