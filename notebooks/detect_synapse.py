import os
import numpy as np
import tifffile
import pandas as pd
from skimage.feature import blob_log
from skimage import exposure
from skimage.transform import resize

input_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"
output_folder = r"D:\Conn_3dpipeline\results\C00_synquant2"

os.makedirs(output_folder, exist_ok=True)

files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    output_path = os.path.join(output_folder, filename + "_results.csv")
    
    try:
        img = tifffile.imread(os.path.join(input_folder, filename))
        
        # Auto contrast
        p2, p98 = np.percentile(img, (2, 98))
        img_norm = exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))
        
        # Downsample to 50% for faster detection
        img_small = resize(img_norm, (img_norm.shape[0]//2, img_norm.shape[1]//2),
                          anti_aliasing=True)
        
        # Detect blobs
        blobs = blob_log(img_small, min_sigma=1, max_sigma=5,
                        num_sigma=5, threshold=0.05)
        
        if len(blobs) > 0:
            # Scale coordinates back to original size
            blobs[:, 0] *= 2  # Y
            blobs[:, 1] *= 2  # X
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