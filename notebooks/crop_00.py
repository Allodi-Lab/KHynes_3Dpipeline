import os
import tifffile

input_folder = r"D:\Conn_3dpipeline\raw_converted_C00_converted"
output_folder = r"D:\Conn_3dpipeline\raw_converted_C00_cropped"

os.makedirs(output_folder, exist_ok=True)

x = 6588
y = 252
w = 4992
h = 7740

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