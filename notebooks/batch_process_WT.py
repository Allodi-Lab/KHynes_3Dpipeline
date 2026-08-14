from cellpose import models
import torch
import os
import tifffile

device = torch.device('cuda')
model = models.CellposeModel(
    pretrained_model=r"C:\Users\zeiss\.cellpose\models\custom",
    device=device
)

input_folder = r"D:\Conn_3dpipeline\WT\raw_C02_converted"
output_folder = r"D:\Conn_3dpipeline\WT\masks"

files = sorted([f for f in os.listdir(input_folder) if f.endswith('.tif')])
print(f"Found {len(files)} files")

for i, filename in enumerate(files):
    mask_name = filename.replace('.tif', '_cp_masks.tif')
    mask_path = os.path.join(output_folder, mask_name)
    
    if os.path.exists(mask_path):
        print(f"Skipping {i+1}/{len(files)}: {filename}")
        continue
    
    input_path = os.path.join(input_folder, filename)
    img = tifffile.imread(input_path)
    masks, flows, styles = model.eval(
        img,
        diameter=28,
        cellprob_threshold=-1
    )
    tifffile.imwrite(mask_path, masks.astype('uint16'))
    print(f"Processed {i+1}/{len(files)}: {filename}")

print("Done")