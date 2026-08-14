import imagej
import os
import time
import pandas as pd
from roifile import ImagejRoi

ij = imagej.init(r"C:\Users\zeiss\Fiji.app_full\Fiji", mode="interactive")

input_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"
output_folder = r"D:\Conn_3dpipeline\results\C00_synquant"
temp_zip = r"D:/Conn_3dpipeline/results/C00_synquant/temp_rois.zip"

files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    output_path = os.path.join(output_folder, filename + "_results.csv")
    
    if os.path.exists(output_path):
        print(f"Skipping {i+1}/{len(files)}: {filename}")
        continue
    
    print(f"Processing {i+1}/{len(files)}: {filename}")
    input_path = os.path.join(input_folder, filename).replace("\\", "/")
    
    macro = f"""
roiManager("reset");
run("Close All");
open("{input_path}");
run("Enhance Contrast", "saturated=0.35");
run("SynQuantVid ", "z-score=10 min=10 max=200 min_0=0.50 max_0=4 post-synapse=Null pre-synapse={filename} way=Null dendrite=Null extended=0 z=1 zscore=10");
wait(2000);
roiManager("Save", "{temp_zip}");
roiManager("reset");
run("Close All");
"""
    
    ij.py.run_macro(macro)
    time.sleep(5)
    
    try:
        if os.path.exists(temp_zip):
            rois = ImagejRoi.fromfile(temp_zip)
            if not isinstance(rois, list):
                rois = [rois]
            rows = []
            for roi in rois:
                rows.append({
                    'X': roi.left,
                    'Y': roi.top,
                    'Width': roi.right - roi.left,
                    'Height': roi.bottom - roi.top
                })
            df = pd.DataFrame(rows)
            df.to_csv(output_path, index=False)
            os.remove(temp_zip)
            print(f"Saved {len(df)} synapses for {filename}")
        else:
            print(f"No synapses found in {filename} â€” saving empty CSV")
            pd.DataFrame(columns=['X','Y','Width','Height']).to_csv(output_path, index=False)
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        pd.DataFrame(columns=['X','Y','Width','Height']).to_csv(output_path, index=False)

print("Done")