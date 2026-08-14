import os
import tifffile

input_folder = r"D:\Conn_3dpipeline\WT\raw_WT_C01_converted"
output_folder = r"D:\Conn_3dpipeline\WT\raw_WT_C01_cropped"

os.makedirs(output_folder, exist_ok=True)

x = 6012
y = 336
w = 4044
h = 10908

files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    try:
        img = tifffile.imread(input_path)
        cropped = img[y:y+h, x:x+w]
        tifffile.imwrite(output_path, cropped)
        print(f"Cropped {i+1}/{len(files)}: {filename}")
    except Exception as e:
        print(f"Failed: {filename} — {e}")

print("Done")