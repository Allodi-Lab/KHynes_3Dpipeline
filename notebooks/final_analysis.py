import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os


# ============================================================
# SETTINGS
# ============================================================

output_folder = r"D:\Conn_3dpipeline\results\statistics"

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
# COLUMN NAMES
# ============================================================

glyt2_count_column = "GlyT2_synapse_count"

geph_count_column = "Gephyrin_synapse_count"


# ============================================================
# LOAD DATA
# ============================================================

print("============================================================")
print("LOADING DATA")
print("============================================================")

glyt2_df = pd.read_csv(glyt2_path)

geph_df = pd.read_csv(geph_path)

print()
print(f"GlyT2 rows loaded: {len(glyt2_df)}")
print(f"Gephyrin rows loaded: {len(geph_df)}")


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_glyt2 = [
    'Z_slice',
    'neuron_id',
    'neuron_x',
    'neuron_y',
    glyt2_count_column
]

required_geph = [
    'Z_slice',
    'neuron_id',
    'neuron_x',
    'neuron_y',
    geph_count_column
]


for column in required_glyt2:

    if column not in glyt2_df.columns:

        raise ValueError(
            f"GlyT2 CSV is missing column: {column}"
        )


for column in required_geph:

    if column not in geph_df.columns:

        raise ValueError(
            f"Gephyrin CSV is missing column: {column}"
        )


print()
print("All required columns found.")


# ============================================================
# CLEAN DATA
# ============================================================

print()
print("============================================================")
print("CLEANING DATA")
print("============================================================")


# Convert Z slice to numeric

glyt2_df['Z_slice'] = pd.to_numeric(
    glyt2_df['Z_slice'],
    errors='coerce'
)

geph_df['Z_slice'] = pd.to_numeric(
    geph_df['Z_slice'],
    errors='coerce'
)


# Convert neuron IDs to numeric

glyt2_df['neuron_id'] = pd.to_numeric(
    glyt2_df['neuron_id'],
    errors='coerce'
)

geph_df['neuron_id'] = pd.to_numeric(
    geph_df['neuron_id'],
    errors='coerce'
)


# Convert synapse counts to numeric

glyt2_df[glyt2_count_column] = pd.to_numeric(
    glyt2_df[glyt2_count_column],
    errors='coerce'
)

geph_df[geph_count_column] = pd.to_numeric(
    geph_df[geph_count_column],
    errors='coerce'
)


# Remove rows with missing essential information

glyt2_df = glyt2_df.dropna(
    subset=[
        'Z_slice',
        'neuron_id',
        glyt2_count_column
    ]
)

geph_df = geph_df.dropna(
    subset=[
        'Z_slice',
        'neuron_id',
        geph_count_column
    ]
)


# Convert identifiers to integers

glyt2_df['Z_slice'] = (
    glyt2_df['Z_slice'].astype(int)
)

geph_df['Z_slice'] = (
    geph_df['Z_slice'].astype(int)
)

glyt2_df['neuron_id'] = (
    glyt2_df['neuron_id'].astype(int)
)

geph_df['neuron_id'] = (
    geph_df['neuron_id'].astype(int)
)


print(
    f"Clean GlyT2 rows: {len(glyt2_df)}"
)

print(
    f"Clean Gephyrin rows: {len(geph_df)}"
)


# ============================================================
# CHECK FOR DUPLICATE NEURONS
# ============================================================

print()
print("============================================================")
print("CHECKING FOR DUPLICATES")
print("============================================================")


duplicate_glyt2 = glyt2_df.duplicated(
    subset=[
        'Z_slice',
        'neuron_id'
    ]
).sum()


duplicate_geph = geph_df.duplicated(
    subset=[
        'Z_slice',
        'neuron_id'
    ]
).sum()


print(
    f"Duplicate GlyT2 entries: {duplicate_glyt2}"
)

print(
    f"Duplicate Gephyrin entries: {duplicate_geph}"
)


if duplicate_glyt2 > 0:

    raise ValueError(
        "Duplicate Z_slice + neuron_id combinations "
        "were found in the GlyT2 CSV."
    )


if duplicate_geph > 0:

    raise ValueError(
        "Duplicate Z_slice + neuron_id combinations "
        "were found in the Gephyrin CSV."
    )


# ============================================================
# MATCH GLYT2 AND GEPHYRIN NEURONS
# ============================================================

print()
print("============================================================")
print("MATCHING NEURONS")
print("============================================================")


paired_df = pd.merge(

    glyt2_df[
        [
            'Z_slice',
            'neuron_id',
            'neuron_x',
            'neuron_y',
            glyt2_count_column
        ]
    ],

    geph_df[
        [
            'Z_slice',
            'neuron_id',
            geph_count_column
        ]
    ],

    on=[
        'Z_slice',
        'neuron_id'
    ],

    how='inner'

)


# Rename columns

paired_df = paired_df.rename(

    columns={

        glyt2_count_column:
            'GlyT2_synapse_count',

        geph_count_column:
            'Gephyrin_synapse_count'

    }

)


print(
    f"GlyT2 neurons: {len(glyt2_df)}"
)

print(
    f"Gephyrin neurons: {len(geph_df)}"
)

print(
    f"Paired neurons: {len(paired_df)}"
)


if len(paired_df) == 0:

    raise ValueError(
        "No matching neurons were found."
    )


# ============================================================
# EXTRACT COUNTS
# ============================================================

glyt2 = paired_df[
    'GlyT2_synapse_count'
]

geph = paired_df[
    'Gephyrin_synapse_count'
]


# ============================================================
# CALCULATE GLYT2 : GEPHYRIN RATIO
# ============================================================

paired_df['GlyT2_Gephyrin_ratio'] = np.where(

    paired_df[
        'Gephyrin_synapse_count'
    ] > 0,

    paired_df[
        'GlyT2_synapse_count'
    ]
    /
    paired_df[
        'Gephyrin_synapse_count'
    ],

    np.nan

)


ratio_mean = (
    paired_df[
        'GlyT2_Gephyrin_ratio'
    ].mean()
)


ratio_median = (
    paired_df[
        'GlyT2_Gephyrin_ratio'
    ].median()
)


# ============================================================
# STATISTICAL TESTS
# ============================================================

print()
print("============================================================")
print("STATISTICAL ANALYSIS")
print("============================================================")


# ------------------------------------------------------------
# Wilcoxon signed-rank test
# ------------------------------------------------------------

wilcoxon_stat, wilcoxon_p = stats.wilcoxon(

    glyt2,

    geph

)


print()
print("Wilcoxon signed-rank test")

print(
    f"Statistic: {wilcoxon_stat:.4f}"
)

print(
    f"P-value: {wilcoxon_p:.6e}"
)


# ------------------------------------------------------------
# Spearman correlation
# ------------------------------------------------------------

spearman_rho, spearman_p = stats.spearmanr(

    glyt2,

    geph

)


print()
print("Spearman correlation")

print(
    f"Rho: {spearman_rho:.4f}"
)

print(
    f"P-value: {spearman_p:.6e}"
)


# ============================================================
# 1. FINAL ANALYSIS SUMMARY
# ============================================================

print()
print("============================================================")
print("CREATING FINAL SUMMARY")
print("============================================================")


final_summary = pd.DataFrame({

    'Metric': [

        'Paired neurons',

        'Total GlyT2 synapses',

        'Total Gephyrin synapses',

        'Mean GlyT2 synapses/neuron',

        'Mean Gephyrin synapses/neuron',

        'Median GlyT2 synapses/neuron',

        'Median Gephyrin synapses/neuron',

        'GlyT2 standard deviation',

        'Gephyrin standard deviation',

        'Minimum GlyT2 synapses/neuron',

        'Minimum Gephyrin synapses/neuron',

        'Maximum GlyT2 synapses/neuron',

        'Maximum Gephyrin synapses/neuron',

        'Mean GlyT2:Gephyrin ratio',

        'Median GlyT2:Gephyrin ratio',

        'Wilcoxon statistic',

        'Wilcoxon p-value',

        'Spearman rho',

        'Spearman p-value'

    ],

    'Value': [

        len(paired_df),

        int(glyt2.sum()),

        int(geph.sum()),

        round(glyt2.mean(), 3),

        round(geph.mean(), 3),

        round(glyt2.median(), 3),

        round(geph.median(), 3),

        round(glyt2.std(), 3),

        round(geph.std(), 3),

        int(glyt2.min()),

        int(geph.min()),

        int(glyt2.max()),

        int(geph.max()),

        round(ratio_mean, 3),

        round(ratio_median, 3),

        round(wilcoxon_stat, 4),

        wilcoxon_p,

        round(spearman_rho, 4),

        spearman_p

    ]

})


final_summary_path = os.path.join(

    output_folder,

    'FINAL_ANALYSIS_SUMMARY.csv'

)


final_summary.to_csv(

    final_summary_path,

    index=False

)


print(
    f"Saved: {final_summary_path}"
)


# ============================================================
# SAVE COMPLETE PAIRED DATASET
# ============================================================

paired_output_path = os.path.join(

    output_folder,

    'paired_neuron_statistics.csv'

)


paired_df.to_csv(

    paired_output_path,

    index=False

)


print(
    f"Saved: {paired_output_path}"
)


# ============================================================
# 2. PAIRED NEURON COMPARISON PLOT
# ============================================================

print()
print("============================================================")
print("CREATING PAIRED NEURON PLOT")
print("============================================================")


plot_df = paired_df.copy()


# Sort by GlyT2 count

plot_df = plot_df.sort_values(

    'GlyT2_synapse_count'

).reset_index(
    drop=True
)


# If there are more than 200 neurons,
# show the first 200 for readability.

if len(plot_df) > 200:

    plot_df = plot_df.iloc[:200]

    print(
        "More than 200 neurons detected."
    )

    print(
        "Plot limited to first 200 neurons "
        "for readability."
    )


fig, ax = plt.subplots(

    figsize=(14, 7)

)


x_positions = np.arange(

    len(plot_df)

)


# Connect GlyT2 and Gephyrin measurements

for i in range(

    len(plot_df)

):

    ax.plot(

        [
            x_positions[i],
            x_positions[i]
        ],

        [

            plot_df.loc[
                i,
                'GlyT2_synapse_count'
            ],

            plot_df.loc[
                i,
                'Gephyrin_synapse_count'
            ]

        ],

        color='gray',

        alpha=0.35,

        linewidth=0.8

    )


# GlyT2 points

ax.scatter(

    x_positions,

    plot_df[
        'GlyT2_synapse_count'
    ],

    s=20,

    label='GlyT2'

)


# Gephyrin points

ax.scatter(

    x_positions,

    plot_df[
        'Gephyrin_synapse_count'
    ],

    s=20,

    label='Gephyrin'

)


ax.set_xlabel(

    'Individual neurons',

    fontsize=12

)


ax.set_ylabel(

    'Synapse count per neuron',

    fontsize=12

)


ax.set_title(

    'Paired GlyT2 and Gephyrin Synapse Counts',

    fontsize=14

)


ax.legend()


plt.tight_layout()


paired_plot_path = os.path.join(

    output_folder,

    'paired_neuron_comparison.png'

)


plt.savefig(

    paired_plot_path,

    dpi=300

)


plt.show()


print(
    f"Saved: {paired_plot_path}"
)


# ============================================================
# 3. PER-Z-SLICE STATISTICS
# ============================================================

print()
print("============================================================")
print("CALCULATING Z-SLICE STATISTICS")
print("============================================================")


slice_stats = (

    paired_df

    .groupby('Z_slice')

    .agg(

        Number_of_neurons=(

            'neuron_id',

            'count'

        ),

        GlyT2_mean=(

            'GlyT2_synapse_count',

            'mean'

        ),

        GlyT2_median=(

            'GlyT2_synapse_count',

            'median'

        ),

        GlyT2_total=(

            'GlyT2_synapse_count',

            'sum'

        ),

        Gephyrin_mean=(

            'Gephyrin_synapse_count',

            'mean'

        ),

        Gephyrin_median=(

            'Gephyrin_synapse_count',

            'median'

        ),

        Gephyrin_total=(

            'Gephyrin_synapse_count',

            'sum'

        )

    )

)


slice_stats = slice_stats.reset_index()


slice_stats = slice_stats.round(3)


slice_stats_path = os.path.join(

    output_folder,

    'synapse_statistics_by_Z_slice.csv'

)


slice_stats.to_csv(

    slice_stats_path,

    index=False

)


print(
    f"Saved: {slice_stats_path}"
)


# ============================================================
# 4. Z-SLICE PLOT
# ============================================================

print()
print("============================================================")
print("CREATING Z-SLICE PLOT")
print("============================================================")


fig, ax = plt.subplots(

    figsize=(14, 7)

)


ax.plot(

    slice_stats['Z_slice'],

    slice_stats['GlyT2_mean'],

    linewidth=2,

    label='GlyT2'

)


ax.plot(

    slice_stats['Z_slice'],

    slice_stats['Gephyrin_mean'],

    linewidth=2,

    label='Gephyrin'

)


ax.set_xlabel(

    'Z Slice',

    fontsize=12

)


ax.set_ylabel(

    'Mean Synapses per Neuron',

    fontsize=12

)


ax.set_title(

    'Synapse Counts Across Tissue Depth',

    fontsize=14

)


ax.legend()


plt.tight_layout()


slice_plot_path = os.path.join(

    output_folder,

    'synapse_counts_by_Z_slice.png'

)


plt.savefig(

    slice_plot_path,

    dpi=300

)


plt.show()


print(
    f"Saved: {slice_plot_path}"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("============================================================")
print("FINAL ANALYSIS COMPLETE")
print("============================================================")

print()

print(
    f"Paired neurons: {len(paired_df)}"
)

print(
    f"Total GlyT2 synapses: {int(glyt2.sum())}"
)

print(
    f"Total Gephyrin synapses: {int(geph.sum())}"
)

print(
    f"Mean GlyT2 synapses/neuron: "
    f"{glyt2.mean():.2f}"
)

print(
    f"Mean Gephyrin synapses/neuron: "
    f"{geph.mean():.2f}"
)

print(
    f"Median GlyT2 synapses/neuron: "
    f"{glyt2.median():.2f}"
)

print(
    f"Median Gephyrin synapses/neuron: "
    f"{geph.median():.2f}"
)

print(
    f"Wilcoxon p-value: "
    f"{wilcoxon_p:.6e}"
)

print(
    f"Spearman rho: "
    f"{spearman_rho:.4f}"
)

print(
    f"Spearman p-value: "
    f"{spearman_p:.6e}"
)

print(
    f"Mean GlyT2:Gephyrin ratio: "
    f"{ratio_mean:.3f}"
)

print(
    f"Median GlyT2:Gephyrin ratio: "
    f"{ratio_median:.3f}"
)

print()
print("Output folder:")
print(output_folder)

print()
print("Files created:")

print(
    " - FINAL_ANALYSIS_SUMMARY.csv"
)

print(
    " - paired_neuron_statistics.csv"
)

print(
    " - synapse_statistics_by_Z_slice.csv"
)

print(
    " - paired_neuron_comparison.png"
)

print(
    " - synapse_counts_by_Z_slice.png"
)

print()
print("Done.")