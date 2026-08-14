import tifffile
import os

input_folder = r"D:\Conn_3dpipeline\WT\raw_WT_C01"
output_folder = r"D:\Conn_3dpipeline\WT\raw_WT_C01_converted"

os.makedirs(output_folder, exist_ok=True)

files = [f for f in os.listdir(input_folder) if f.endswith('.tif')]
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename.replace('.ome.tif', '.tif'))
    
    try:
        img = tifffile.imread(input_path)
        tifffile.imwrite(output_path, img)
        print(f"Converted {i+1}/{len(files)}: {filename}")
    except Exception as e:
        print(f"Failed: {filename} — {e}")

print("Done")