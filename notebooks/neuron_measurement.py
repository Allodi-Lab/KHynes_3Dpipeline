import pandas as pd
import numpy as np
import tifffile
import os


# ============================================================
# SETTINGS
# ============================================================

output_folder = r"D:\Conn_3dpipeline\results\neuron_measurements"

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# FILE PATHS
# ============================================================

glyt2_path = (
    r"D:\Conn_3dpipeline\results\matching"
    r"\TDP43_synapse_counts.csv"
)

geph_path = (
    r"D:\Conn_3dpipeline\results\matching"
    r"\TDP43_gephyrin_counts.csv"
)


# ============================================================
# LOAD MATCHING RESULTS
# ============================================================

print("Loading GlyT2 matching results...")

glyt2_df = pd.read_csv(glyt2_path)

print(
    f"GlyT2 rows loaded: {len(glyt2_df)}"
)


print("Loading Gephyrin matching results...")

geph_df = pd.read_csv(geph_path)

print(
    f"Gephyrin rows loaded: {len(geph_df)}"
)


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_glyt2 = [
    'Z_slice',
    'neuron_id',
    'GlyT2_synapse_count'
]

required_geph = [
    'Z_slice',
    'neuron_id',
    'Gephyrin_synapse_count'
]


for column in required_glyt2:

    if column not in glyt2_df.columns:

        raise ValueError(
            f"GlyT2 CSV is missing required column: {column}"
        )


for column in required_geph:

    if column not in geph_df.columns:

        raise ValueError(
            f"Gephyrin CSV is missing required column: {column}"
        )


# ============================================================
# CLEAN DATA
# ============================================================

glyt2_df['Z_slice'] = pd.to_numeric(
    glyt2_df['Z_slice'],
    errors='coerce'
)

geph_df['Z_slice'] = pd.to_numeric(
    geph_df['Z_slice'],
    errors='coerce'
)


glyt2_df['neuron_id'] = pd.to_numeric(
    glyt2_df['neuron_id'],
    errors='coerce'
)

geph_df['neuron_id'] = pd.to_numeric(
    geph_df['neuron_id'],
    errors='coerce'
)


glyt2_df['GlyT2_synapse_count'] = pd.to_numeric(
    glyt2_df['GlyT2_synapse_count'],
    errors='coerce'
)

geph_df['Gephyrin_synapse_count'] = pd.to_numeric(
    geph_df['Gephyrin_synapse_count'],
    errors='coerce'
)


glyt2_df = glyt2_df.dropna(
    subset=[
        'Z_slice',
        'neuron_id',
        'GlyT2_synapse_count'
    ]
)

geph_df = geph_df.dropna(
    subset=[
        'Z_slice',
        'neuron_id',
        'Gephyrin_synapse_count'
    ]
)


# Convert identifiers to integers

glyt2_df['Z_slice'] = glyt2_df['Z_slice'].astype(int)
geph_df['Z_slice'] = geph_df['Z_slice'].astype(int)

glyt2_df['neuron_id'] = glyt2_df['neuron_id'].astype(int)
geph_df['neuron_id'] = geph_df['neuron_id'].astype(int)


# ============================================================
# MERGE GLYT2 AND GEPHYRIN
# ============================================================

print()
print("Matching GlyT2 and Gephyrin measurements...")

neuron_df = pd.merge(

    glyt2_df[
        [
            'Z_slice',
            'neuron_id',
            'GlyT2_synapse_count'
        ]
    ],

    geph_df[
        [
            'Z_slice',
            'neuron_id',
            'Gephyrin_synapse_count'
        ]
    ],

    on=[
        'Z_slice',
        'neuron_id'
    ],

    how='outer'
)


# Replace missing synapse counts with zero

neuron_df['GlyT2_synapse_count'] = (
    neuron_df['GlyT2_synapse_count']
    .fillna(0)
)

neuron_df['Gephyrin_synapse_count'] = (
    neuron_df['Gephyrin_synapse_count']
    .fillna(0)
)


# ============================================================
# CALCULATE SYNAPSE RATIOS
# ============================================================

neuron_df['GlyT2_Gephyrin_ratio'] = np.where(

    neuron_df['Gephyrin_synapse_count'] > 0,

    neuron_df['GlyT2_synapse_count']
    / neuron_df['Gephyrin_synapse_count'],

    np.nan
)


# ============================================================
# CALCULATE SYNAPSE DIFFERENCE
# ============================================================

neuron_df['GlyT2_minus_Gephyrin'] = (

    neuron_df['GlyT2_synapse_count']
    - neuron_df['Gephyrin_synapse_count']

)


# ============================================================
# LOAD NEURON MASKS AND CALCULATE AREA
# ============================================================

print()
print("Calculating neuron areas from masks...")


# ------------------------------------------------------------
# MASK SETTINGS
# ------------------------------------------------------------

mask_folder = r"D:\Conn_3dpipeline\masks"


mask_prefix = (
    "14-23-20_382_NF-780_Glyt2-647_Gef-555-nf-488_"
    "2763um_z-3um_tiles_DSI_12x_2-5x_Blaze_C02_"
)


# ------------------------------------------------------------
# CROP COORDINATES
# ------------------------------------------------------------

x = 6588
y = 252
w = 4992
h = 7740


# ------------------------------------------------------------
# GET Z SLICES
# ------------------------------------------------------------

z_slices = sorted(
    neuron_df['Z_slice'].unique()
)


area_records = []


for z_slice in z_slices:

    # Convert numeric slice to filename format
    z_num = f"Z{int(z_slice):04d}"

    mask_file = (
        mask_prefix
        + z_num
        + "_cp_masks.tif"
    )

    mask_path = os.path.join(
        mask_folder,
        mask_file
    )


    # --------------------------------------------------------
    # CHECK MASK EXISTS
    # --------------------------------------------------------

    if not os.path.exists(mask_path):

        print(
            f"WARNING: Mask not found for {z_num}"
        )

        continue


    # --------------------------------------------------------
    # LOAD MASK
    # --------------------------------------------------------

    mask = tifffile.imread(
        mask_path
    )


    # --------------------------------------------------------
    # CROP MASK
    # --------------------------------------------------------

    mask_cropped = mask[
        y:y+h,
        x:x+w
    ]


    # --------------------------------------------------------
    # CALCULATE AREA FOR EACH NEURON
    # --------------------------------------------------------

    neuron_ids = np.unique(
        mask_cropped
    )

    neuron_ids = neuron_ids[
        neuron_ids > 0
    ]


    for neuron_id in neuron_ids:

        area_pixels = np.sum(
            mask_cropped == neuron_id
        )


        area_records.append({

            'Z_slice': int(z_slice),

            'neuron_id': int(neuron_id),

            'neuron_area_pixels': int(
                area_pixels
            )

        })


# ============================================================
# CREATE AREA DATAFRAME
# ============================================================

area_df = pd.DataFrame(
    area_records
)


# ============================================================
# MERGE AREA WITH SYNAPSE DATA
# ============================================================

neuron_df = pd.merge(

    neuron_df,

    area_df,

    on=[
        'Z_slice',
        'neuron_id'
    ],

    how='left'
)


# ============================================================
# CALCULATE SYNAPSE DENSITY
# ============================================================

neuron_df['GlyT2_density'] = np.where(

    neuron_df['neuron_area_pixels'] > 0,

    neuron_df['GlyT2_synapse_count']
    / neuron_df['neuron_area_pixels'],

    np.nan
)


neuron_df['Gephyrin_density'] = np.where(

    neuron_df['neuron_area_pixels'] > 0,

    neuron_df['Gephyrin_synapse_count']
    / neuron_df['neuron_area_pixels'],

    np.nan
)


# ============================================================
# SORT DATA
# ============================================================

neuron_df = neuron_df.sort_values(

    by=[
        'Z_slice',
        'neuron_id'
    ]

)


# ============================================================
# ROUND MEASUREMENTS
# ============================================================

neuron_df['GlyT2_Gephyrin_ratio'] = (
    neuron_df['GlyT2_Gephyrin_ratio']
    .round(3)
)

neuron_df['GlyT2_density'] = (
    neuron_df['GlyT2_density']
    .round(6)
)

neuron_df['Gephyrin_density'] = (
    neuron_df['Gephyrin_density']
    .round(6)
)


# ============================================================
# SAVE PER-NEURON DATA
# ============================================================

neuron_output_path = os.path.join(

    output_folder,

    'per_neuron_measurements.csv'

)


neuron_df.to_csv(

    neuron_output_path,

    index=False

)


print()
print(
    f"Saved per-neuron measurements:"
)

print(
    neuron_output_path
)


# ============================================================
# MATCHING QUALITY
# ============================================================

print()
print("============================================================")
print("MATCHING QUALITY")
print("============================================================")


# ------------------------------------------------------------
# GLYT2
# ------------------------------------------------------------

total_glyt2 = int(
    glyT2_total := glyt2_df[
        'GlyT2_synapse_count'
    ].sum()
)


matched_glyt2 = int(
    neuron_df[
        'GlyT2_synapse_count'
    ].sum()
)


unmatched_glyt2 = (
    total_glyt2
    - matched_glyt2
)


if total_glyt2 > 0:

    glyt2_match_rate = (
        matched_glyt2
        / total_glyt2
        * 100
    )

else:

    glyt2_match_rate = 0


# ------------------------------------------------------------
# GEPHYRIN
# ------------------------------------------------------------

total_geph = int(
    geph_df[
        'Gephyrin_synapse_count'
    ].sum()
)


matched_geph = int(
    neuron_df[
        'Gephyrin_synapse_count'
    ].sum()
)


unmatched_geph = (
    total_geph
    - matched_geph
)


if total_geph > 0:

    geph_match_rate = (
        matched_geph
        / total_geph
        * 100
    )

else:

    geph_match_rate = 0


# ============================================================
# PRINT MATCHING RESULTS
# ============================================================

print()

print("GlyT2")
print("----------------------------")

print(
    f"Total detected: {total_glyt2}"
)

print(
    f"Matched: {matched_glyt2}"
)

print(
    f"Unmatched: {unmatched_glyt2}"
)

print(
    f"Match rate: {glyt2_match_rate:.2f}%"
)


print()

print("Gephyrin")
print("----------------------------")

print(
    f"Total detected: {total_geph}"
)

print(
    f"Matched: {matched_geph}"
)

print(
    f"Unmatched: {unmatched_geph}"
)

print(
    f"Match rate: {geph_match_rate:.2f}%"
)


# ============================================================
# SAVE MATCHING QUALITY CSV
# ============================================================

matching_quality_df = pd.DataFrame({

    'Marker': [

        'GlyT2',

        'Gephyrin'

    ],

    'Total detected synapses': [

        total_glyt2,

        total_geph

    ],

    'Matched synapses': [

        matched_glyt2,

        matched_geph

    ],

    'Unmatched synapses': [

        unmatched_glyt2,

        unmatched_geph

    ],

    'Match rate (%)': [

        round(
            glyt2_match_rate,
            2
        ),

        round(
            geph_match_rate,
            2
        )

    ]

})


matching_quality_path = os.path.join(

    output_folder,

    'matching_quality.csv'

)


matching_quality_df.to_csv(

    matching_quality_path,

    index=False

)


print()
print(
    f"Saved matching quality:"
)

print(
    matching_quality_path
)


# ============================================================
# PRINT PER-NEURON SUMMARY
# ============================================================

print()
print("============================================================")
print("PER-NEURON MEASUREMENT SUMMARY")
print("============================================================")

print(
    f"Total neurons measured: "
    f"{len(neuron_df)}"
)

print(
    f"Mean neuron area (pixels): "
    f"{neuron_df['neuron_area_pixels'].mean():.2f}"
)

print(
    f"Mean GlyT2 synapses/neuron: "
    f"{neuron_df['GlyT2_synapse_count'].mean():.2f}"
)

print(
    f"Mean Gephyrin synapses/neuron: "
    f"{neuron_df['Gephyrin_synapse_count'].mean():.2f}"
)

print(
    f"Mean GlyT2 density: "
    f"{neuron_df['GlyT2_density'].mean():.6f}"
)

print(
    f"Mean Gephyrin density: "
    f"{neuron_df['Gephyrin_density'].mean():.6f}"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("============================================================")
print("NEURON MEASUREMENT ANALYSIS COMPLETE")
print("============================================================")

print()
print("Files created:")

print(
    "1. per_neuron_measurements.csv"
)

print(
    "2. matching_quality.csv"
)

print()
print("Output folder:")

print(
    output_folder
)