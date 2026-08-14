import tifffile
import numpy as np

volume=tifffile.imread(r"D:\Conn_3dpipeline\results\neurons_3d.tif")
print(f"Volume Shape: {volume.shape}")
print(f"Volume dtype: {volume.dtype}")
print(f"Unique Values: {len(np.unique(volume))}")
print(f"Max Value: {volume.max()}")