import tifffile
import numpy as np
import matplotlib.pyplot as plt
import imageio
from skimage import exposure
from skimage.color import label2rgb
import pandas as pd
import os

z_num = "Z0631"

c00_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif"
mask_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}_cp_masks.tif"
csv_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C00_{z_num}.tif_results.csv"

c00_path = os.path.join(r"D:\Conn_3dpipeline\raw_converted_C00_cropped", c00_file)
mask_path = os.path.join(r"D:\Conn_3dpipeline\masks", mask_file)
csv_path = os.path.join(r"D:\Conn_3dpipeline\results\C00_synquant2", csv_file)

def auto_contrast(img):
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img.astype(float), in_range=(p2, p98))

x, y, w, h = 6588, 252, 4992, 7740

print("Loading images...")
c00 = tifffile.imread(c00_path)
c00_norm = auto_contrast(c00)
c00_norm = c00_norm / c00_norm.max()

# Blue tinted background
c00_rgb = np.stack([c00_norm * 0.3, c00_norm * 0.6, c00_norm], axis=-1)

mask = tifffile.imread(mask_path)
mask_cropped = mask[y:y+h, x:x+w]

# Colored neuron overlay
overlay = label2rgb(mask_cropped, image=c00_rgb, bg_label=0, alpha=0.5)
neuron_count = len(np.unique(mask_cropped)) - 1

# Load synaptic dots
df = pd.read_csv(csv_path) if os.path.exists(csv_path) else pd.DataFrame(columns=['X','Y'])

print(f"Neurons: {neuron_count}, Synaptic dots: {len(df)}")

fig, axes = plt.subplots(1, 2, figsize=(20, 10))
fig.patch.set_facecolor('black')

frames = []

def add_frame(left_img, left_title, right_img, right_title, dots_alpha=0.0, hold=False):
    axes[0].cla()
    axes[1].cla()
    axes[0].imshow(np.clip(left_img, 0, 1))
    axes[0].set_title(left_title, color='white', fontsize=12)
    axes[0].axis('off')
    axes[0].set_facecolor('black')
    axes[1].imshow(np.clip(right_img, 0, 1))
    if dots_alpha > 0 and len(df) > 0:
        axes[1].scatter(df['X'], df['Y'], c='yellow', s=3, alpha=dots_alpha)
    axes[1].set_title(right_title, color='white', fontsize=12)
    axes[1].axis('off')
    axes[1].set_facecolor('black')
    fig.canvas.draw()
    frame = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    frame = frame.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    frame = frame[:, :, 1:]
    repeat = 5 if hold else 1
    for _ in range(repeat):
        frames.append(frame)

# ============================================================
# STAGE 1 â€” Show raw spine (hold 1 second)
# ============================================================
plt.suptitle('TDP-43 Spinal Cord - GlyT2 Channel', color='white', fontsize=16)
for _ in range(8):
    add_frame(c00_rgb, 'Spinal Cord Tissue', c00_rgb, 'Spinal Cord Tissue')

# ============================================================
# STAGE 2 â€” Fade in synaptic dots on right panel
# ============================================================
plt.suptitle('TDP-43 - GlyT2 Synaptic Dots Appearing', color='white', fontsize=16)
for alpha in np.linspace(0, 0.9, 15):
    add_frame(c00_rgb, 'Spinal Cord Tissue',
              c00_rgb, f'GlyT2 Synaptic Dots ({len(df)})',
              dots_alpha=alpha)

# Hold with dots visible
for _ in range(8):
    add_frame(c00_rgb, 'Spinal Cord Tissue',
              c00_rgb, f'GlyT2 Synaptic Dots ({len(df)})',
              dots_alpha=0.9)

# ============================================================
# STAGE 3 â€” Fade in neuron overlay on left panel
# ============================================================
plt.suptitle('TDP-43 - Neurons Appearing', color='white', fontsize=16)
for alpha in np.linspace(0, 1, 15):
    blended = alpha * overlay + (1 - alpha) * c00_rgb
    add_frame(blended, f'Segmented Neurons ({neuron_count})',
              c00_rgb, f'GlyT2 Synaptic Dots ({len(df)})',
              dots_alpha=0.9)

# Hold with neurons visible
for _ in range(8):
    add_frame(overlay, f'Segmented Neurons ({neuron_count})',
              c00_rgb, f'GlyT2 Synaptic Dots ({len(df)})',
              dots_alpha=0.9)

# ============================================================
# STAGE 4 â€” Combine both on right panel (neurons + dots together)
# ============================================================
plt.suptitle('TDP-43 - Combined: Neurons + Synaptic Dots', color='white', fontsize=16)
for alpha in np.linspace(0, 1, 15):
    # Right panel transitions from dots-only to neurons+dots
    blended_right = alpha * overlay + (1 - alpha) * c00_rgb
    add_frame(overlay, f'Segmented Neurons ({neuron_count})',
              blended_right, 'Neurons + GlyT2 Dots Combined',
              dots_alpha=0.9)

# ============================================================
# STAGE 5 â€” Final combined view â€” hold
# ============================================================
plt.suptitle('TDP-43 - Neurons + GlyT2 Synaptic Dots', color='white', fontsize=16)
for _ in range(15):
    add_frame(overlay, f'Segmented Neurons ({neuron_count})',
              overlay, 'Neurons + GlyT2 Dots Combined',
              dots_alpha=0.9)

print(f"Saving {len(frames)} frames...")
imageio.mimsave(r"D:\Conn_3dpipeline\results\slice_Z0631_animation.gif",
                frames, fps=8)
plt.close()
print("Done. Saved slice_Z0631_animation.gif")