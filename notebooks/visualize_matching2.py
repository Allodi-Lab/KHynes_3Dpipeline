import tifffile
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
import pandas as pd
import os

z_num = "Z0631"

# ---------------------------------------------------------
# FILE NAMES
# ---------------------------------------------------------

# C01 = Gephyrin
c01_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_{z_num}.tif"

# C02 = neuron mask
mask_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_{z_num}_cp_masks.tif"

# C01 = Gephyrin synapse detection results
csv_file = f"14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C01_{z_num}.tif_results.csv"


# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

c01_path = os.path.join(
    r"D:\Conn_3dpipeline\raw_converted_C01_cropped",
    c01_file
)

mask_path = os.path.join(
    r"D:\Conn_3dpipeline\masks",
    mask_file
)

csv_path = os.path.join(
    r"D:\Conn_3dpipeline\results\C01_synquant",
    csv_file
)

# Matching results for Gephyrin
results_path = r"D:\Conn_3dpipeline\results\matching\TDP43_gephyrin_counts.csv"

# Output figure
output_path = r"D:\Conn_3dpipeline\results\matching_visualization_gephyrin.png"


# ---------------------------------------------------------
# AUTO CONTRAST
# ---------------------------------------------------------

def auto_contrast(img):

    p2, p98 = np.percentile(img, (2, 98))

    return exposure.rescale_intensity(
        img.astype(float),
        in_range=(p2, p98)
    )


# ---------------------------------------------------------
# CROP COORDINATES
# ---------------------------------------------------------

x, y, w, h = 6588, 252, 4992, 7740


# ---------------------------------------------------------
# LOAD C01 IMAGE â€” GEPHYRIN
# ---------------------------------------------------------

print("Loading C01 Gephyrin image...")

c01 = tifffile.imread(c01_path)

print(f"C01 image shape: {c01.shape}")

c01_norm = auto_contrast(c01)

if c01_norm.max() > 0:
    c01_norm = c01_norm / c01_norm.max()


# ---------------------------------------------------------
# LOAD NEURON MASK
# ---------------------------------------------------------

print("Loading neuron mask...")

mask = tifffile.imread(mask_path)

print(f"Mask shape: {mask.shape}")

mask_cropped = mask[y:y+h, x:x+w]

print(f"Cropped mask shape: {mask_cropped.shape}")


# ---------------------------------------------------------
# LOAD GEPHYRIN SYNAPSE DOTS
# ---------------------------------------------------------

print("Loading Gephyrin synapse detections...")

if os.path.exists(csv_path):

    df = pd.read_csv(csv_path)

    print(f"Gephyrin detections loaded: {len(df)}")

else:

    print("WARNING: Gephyrin detection CSV not found.")

    df = pd.DataFrame(columns=['X', 'Y'])


# ---------------------------------------------------------
# LOAD GEPHYRIN MATCHING RESULTS
# ---------------------------------------------------------

print("Loading Gephyrin matching results...")

if not os.path.exists(results_path):

    raise FileNotFoundError(
        f"Matching results file not found:\n{results_path}"
    )

results_df = pd.read_csv(results_path)

print(f"Matching results loaded: {len(results_df)} rows")

print(
    f"Available columns in matching results:\n"
    f"{list(results_df.columns)}"
)


# ---------------------------------------------------------
# GET RESULTS FOR CURRENT Z-SLICE
# ---------------------------------------------------------

z_stripped = z_num.replace('Z', '').lstrip('0') or '0'

slice_results = results_df[
    results_df['Z_slice'].astype(str).str.lstrip('0') == z_stripped
]

print(
    f"Matching results for {z_num}: "
    f"{len(slice_results)} rows"
)


# ---------------------------------------------------------
# GET NEURON CENTROIDS AND GEPHYRIN SYNAPSE COUNTS
# ---------------------------------------------------------

neuron_ids = np.unique(mask_cropped)

# Remove background
neuron_ids = neuron_ids[neuron_ids > 0]

centroids_x = []
centroids_y = []
synapse_counts = []


for nid in neuron_ids:

    # Find all pixels belonging to this neuron
    positions = np.where(mask_cropped == nid)

    # Calculate centroid
    centroids_y.append(np.mean(positions[0]))
    centroids_x.append(np.mean(positions[1]))

    # Get Gephyrin synapse count for this neuron
    count = slice_results[
        slice_results['neuron_id'] == nid
    ]['Gephyrin_synapse_count'].values

    if len(count) > 0:
        synapse_counts.append(count[0])
    else:
        synapse_counts.append(0)


# ---------------------------------------------------------
# PRINT SUMMARY
# ---------------------------------------------------------

print()
print("---------------------------------------------------------")
print("SUMMARY")
print("---------------------------------------------------------")

print(f"Neurons in slice: {len(neuron_ids)}")

print(
    f"Total matched Gephyrin synapses: "
    f"{sum(synapse_counts)}"
)

print(
    f"Mean Gephyrin synapses per neuron: "
    f"{sum(synapse_counts) / len(synapse_counts) if synapse_counts else 0:.2f}"
)

print("---------------------------------------------------------")
print()


# ---------------------------------------------------------
# PLOT
# ---------------------------------------------------------

fig, axes = plt.subplots(
    1,
    2,
    figsize=(24, 12)
)


# =========================================================
# LEFT PANEL
# ALL DETECTED GEPHYRIN SYNAPTIC DOTS
# =========================================================

axes[0].imshow(
    c01_norm,
    cmap='gray'
)

# Plot all detected Gephyrin synapses
if len(df) > 0:

    axes[0].scatter(
        df['X'],
        df['Y'],
        c='yellow',
        s=3,
        alpha=0.5,
        label=f'Gephyrin dots ({len(df)})'
    )


# Plot neuron centroids
if len(centroids_x) > 0:

    axes[0].scatter(
        centroids_x,
        centroids_y,
        c='red',
        s=100,
        marker='o',
        alpha=0.8,
        label=f'Neurons ({len(neuron_ids)})'
    )


axes[0].set_title(
    f'All Gephyrin Detections â€” {z_num}',
    fontsize=14
)

axes[0].legend(
    fontsize=10
)

axes[0].axis('off')


# =========================================================
# RIGHT PANEL
# NEURONS COLOURED BY GEPHYRIN SYNAPSE COUNT
# =========================================================

axes[1].imshow(
    c01_norm,
    cmap='gray'
)

# Show neuron mask
axes[1].imshow(
    mask_cropped > 0,
    alpha=0.15,
    cmap='Reds'
)


# Plot neurons coloured according to Gephyrin count
if len(centroids_x) > 0:

    max_count = max(synapse_counts) if synapse_counts else 1

    # Avoid vmin == vmax
    if max_count == 0:
        max_count = 1

    sc = axes[1].scatter(
        centroids_x,
        centroids_y,
        c=synapse_counts,
        s=300,
        cmap='cool',
        alpha=0.9,
        zorder=5,
        vmin=0,
        vmax=max_count
    )

    plt.colorbar(
        sc,
        ax=axes[1],
        label='Gephyrin synapse count'
    )


axes[1].set_title(
    f'Neurons Coloured by Gephyrin Synapse Count â€” {z_num}',
    fontsize=14
)

axes[1].axis('off')


# ---------------------------------------------------------
# OVERALL FIGURE TITLE
# ---------------------------------------------------------

plt.suptitle(
    f'Gephyrin Matching Results â€” TDP-43 Slice {z_num}',
    fontsize=16
)

plt.tight_layout()


# ---------------------------------------------------------
# SAVE FIGURE
# ---------------------------------------------------------

plt.savefig(
    output_path,
    dpi=150,
    bbox_inches='tight'
)

plt.show()

print(
    f"Saved Gephyrin matching visualization:\n"
    f"{output_path}"
)


# ---------------------------------------------------------
# INTERPRETATION
# ---------------------------------------------------------

# LEFT PANEL:
#
# Shows all detected Gephyrin synaptic dots (yellow) overlaid
# on the C01 Gephyrin image. Red circles mark the centre of
# each segmented neuron.
#
# This panel can be used to visually check that the detected
# Gephyrin synaptic dots and neuron locations are spatially
# aligned correctly.
#
#
# RIGHT PANEL:
#
# Shows each neuron coloured according to the number of
# Gephyrin synaptic dots matched to that neuron.
#
# Blue = fewer Gephyrin synapses
# Pink = more Gephyrin synapses
#
# This represents the output of the Gephyrin
# synapse-to-neuron matching pipeline.