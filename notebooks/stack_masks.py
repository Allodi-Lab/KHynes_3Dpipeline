import tifffile
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

print("Loading 3D volume — sampling every 10th slice...")
volume = tifffile.imread(r"D:\Conn_3dpipeline\results\neurons_3d_fixed.tif")
volume = volume[::10]
print(f"Sampled volume shape: {volume.shape}")

# Find unique neurons slice by slice to save memory
print("Finding unique neurons...")
neuron_ids = set()
for i in range(volume.shape[0]):
    ids = np.unique(volume[i])
    neuron_ids.update(ids[ids > 0].tolist())
neuron_ids = list(neuron_ids)
print(f"Found {len(neuron_ids)} unique neurons")

# Collect voxel positions per neuron
print("Extracting positions...")
all_z, all_y, all_x, all_colors = [], [], [], []
colors = plt.cm.tab20(np.linspace(0, 1, 20))

for idx, nid in enumerate(neuron_ids[:20]):
    positions = np.where(volume == nid)
    step = max(1, len(positions[0]) // 200)
    all_z.extend(positions[0][::step])
    all_y.extend(positions[1][::step])
    all_x.extend(positions[2][::step])
    all_colors.extend([colors[idx % 20]] * len(positions[0][::step]))
    print(f"Neuron {idx+1}/20 done")

all_z = np.array(all_z)
all_y = np.array(all_y)
all_x = np.array(all_x)

print(f"Plotting {len(all_z)} voxels")

fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')

frames = []
for angle in range(0, 360, 5):
    ax.cla()
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.scatter(all_x, all_y, all_z, c=all_colors, s=2, alpha=0.7)
    ax.view_init(elev=20, azim=angle)
    ax.set_axis_off()
    ax.set_title('TDP-43 Motor Neurons — 3D Rotating',
                color='white', fontsize=14, pad=20)
    
    fig.canvas.draw()
    frame = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    frames.append(frame)
    print(f"Frame {angle//5 + 1}/72")

print("Saving gif...")
imageio.mimsave(r"D:\Conn_3dpipeline\results\neurons_3d_rotating.gif",
                frames, fps=10)
plt.close()
print("Done. Saved neurons_3d_rotating.gif")