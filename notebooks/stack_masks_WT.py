import os
import numpy as np
import tifffile
from PIL import Image

masks_folder = r"D:\Conn_3dpipeline\WT\masks_WT"
output_path = r"D:\Conn_3dpipeline\WT\results_WT\neurons_3d_WT.tif"

files = sorted([f for f in os.listdir(masks_folder) 
                if f.endswith('_cp_masks.tif')])

print(f"Found {len(files)} Mask Files")

scale = 0.50

with tifffile.TiffWriter(output_path, bigtiff=True) as tif:
    for i, f in enumerate(files):
        mask = tifffile.imread(os.path.join(masks_folder, f))
        h, w = mask.shape
        new_h, new_w = int(h * scale), int(w * scale)
        mask_pil = Image.fromarray(mask)
        mask_small = np.array(mask_pil.resize((new_w, new_h), Image.NEAREST))
        tif.write(mask_small.astype('uint16'))
        print(f"Written {i+1}/{len(files)}: {f}")
        del mask, mask_pil, mask_small

print("Saved neurons_3d_WT.tif")