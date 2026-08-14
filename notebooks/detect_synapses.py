import os
import numpy as np
import tifffile
import pandas as pd
from skimage.feature import blob_log
from skimage import exposure

input_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"
output_folder = r"D:\Conn_3dpipeline\results\C00_synquant"

os.makedirs(output_folder, exist_ok=True)

files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    output_path = os.path.join(output_folder, filename + "_results.csv")
    
    if os.path.exists(output_path):
        print(f"Skipping {i+1}/{len(files)}: {filename}")
        continue
    
    try:
        img = tifffile.imread(os.path.join(input_folder, filename))
        
        # Normalize image
        img_norm = exposure.rescale_intensity(img.astype(float))
        
        # Detect blobs (synaptic dots)
        blobs = blob_log(img_norm, min_sigma=1, max_sigma=5, 
                        num_sigma=5, threshold=0.05)
        
        if len(blobs) > 0:
            df = pd.DataFrame({
                'Y': blobs[:, 0],
                'X': blobs[:, 1],
                'Width': blobs[:, 2] * 2,
                'Height': blobs[:, 2] * 2
            })
        else:
            df = pd.DataFrame(columns=['X', 'Y', 'Width', 'Height'])
        
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} synapses for {i+1}/{len(files)}: {filename}")
        
    except Exception as e:
        print(f"Failed {filename}: {e}")

print("Done")