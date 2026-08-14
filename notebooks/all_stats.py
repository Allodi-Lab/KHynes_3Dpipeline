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

print("Loading data...")

glyt2_df = pd.read_csv(glyt2_path)

geph_df = pd.read_csv(geph_path)


print(
    f"GlyT2 rows loaded: {len(glyt2_df)}"
)

print(
    f"Gephyrin rows loaded: {len(geph_df)}"
)


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


glyt2_df[glyt2_count_column] = pd.to_numeric(
    glyt2_df[glyt2_count_column],
    errors='coerce'
)

geph_df[geph_count_column] = pd.to_numeric(
    geph_df[geph_count_column],
    errors='coerce'
)


# Remove incomplete rows

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


# ============================================================
# CHECK FOR DUPLICATE NEURON IDENTIFIERS
# ============================================================

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


print()
print("============================================================")
print("DATA QUALITY CHECK")
print("============================================================")

print(
    f"Duplicate GlyT2 neuron entries: "
    f"{duplicate_glyt2}"
)

print(
    f"Duplicate Gephyrin neuron entries: "
    f"{duplicate_geph}"
)


if duplicate_glyt2 > 0:

    raise ValueError(
        "Duplicate Z_slice + neuron_id combinations "
        "were found in the GlyT2 data."
    )


if duplicate_geph > 0:

    raise ValueError(
        "Duplicate Z_slice + neuron_id combinations "
        "were found in the Gephyrin data."
    )


# ============================================================
# MATCH THE SAME NEURONS
# ============================================================

print()
print("Matching neurons between GlyT2 and Gephyrin...")


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


# Rename the columns to cleaner names

paired_df = paired_df.rename(

    columns={

        glyt2_count_column:
            'GlyT2_synapse_count',

        geph_count_column:
            'Gephyrin_synapse_count'

    }

)


print(
    f"Paired neurons: {len(paired_df)}"
)


# ============================================================
# CHECK THAT ALL PAIRED COUNTS ARE VALID
# ============================================================

if len(paired_df) == 0:

    raise ValueError(
        "No matching neurons were found between "
        "the GlyT2 and Gephyrin CSV files."
    )


# ============================================================
# EXTRACT SYNAPSE COUNTS
# ============================================================

glyt2 = paired_df[
    'GlyT2_synapse_count'
]

geph = paired_df[
    'Gephyrin_synapse_count'
]


# ============================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================

print()
print("============================================================")
print("1. DESCRIPTIVE STATISTICS")
print("============================================================")


summary_df = pd.DataFrame({

    'Measure': [

        'Number of paired neurons',

        'Total synapses',

        'Mean synapses per neuron',

        'Median synapses per neuron',

        'Standard deviation',

        'Minimum synapses',

        'Maximum synapses'

    ],

    'GlyT2 (Presynaptic)': [

        len(glyt2),

        int(glyt2.sum()),

        round(glyt2.mean(), 2),

        round(glyt2.median(), 2),

        round(glyt2.std(), 2),

        int(glyt2.min()),

        int(glyt2.max())

    ],

    'Gephyrin (Postsynaptic)': [

        len(geph),

        int(geph.sum()),

        round(geph.mean(), 2),

        round(geph.median(), 2),

        round(geph.std(), 2),

        int(geph.min()),

        int(geph.max())

    ]

})


print(
    summary_df.to_string(
        index=False
    )
)


summary_path = os.path.join(

    output_folder,

    'priority_summary_statistics.csv'

)


summary_df.to_csv(

    summary_path,

    index=False

)


print()
print(
    f"Saved: {summary_path}"
)


# ============================================================
# 2. WILCOXON SIGNED-RANK TEST
# ============================================================

print()
print("============================================================")
print("2. WILCOXON SIGNED-RANK TEST")
print("============================================================")


wilcoxon_stat, wilcoxon_p = stats.wilcoxon(

    glyt2,

    geph

)


print(
    f"Wilcoxon statistic: "
    f"{wilcoxon_stat:.4f}"
)

print(
    f"P-value: "
    f"{wilcoxon_p:.6e}"
)


# Interpretation

if wilcoxon_p < 0.001:

    wilcoxon_interpretation = (
        "Highly significant (p < 0.001)"
    )

elif wilcoxon_p < 0.01:

    wilcoxon_interpretation = (
        "Significant (p < 0.01)"
    )

elif wilcoxon_p < 0.05:

    wilcoxon_interpretation = (
        "Significant (p < 0.05)"
    )

else:

    wilcoxon_interpretation = (
        "Not significant (p >= 0.05)"
    )


print(
    f"Interpretation: "
    f"{wilcoxon_interpretation}"
)


# ============================================================
# 3. SPEARMAN CORRELATION
# ============================================================

print()
print("============================================================")
print("3. SPEARMAN CORRELATION")
print("============================================================")


spearman_rho, spearman_p = stats.spearmanr(

    glyt2,

    geph

)


print(
    f"Spearman rho: "
    f"{spearman_rho:.4f}"
)

print(
    f"P-value: "
    f"{spearman_p:.6e}"
)


# Interpretation

if spearman_p < 0.001:

    spearman_interpretation = (
        "Highly significant (p < 0.001)"
    )

elif spearman_p < 0.01:

    spearman_interpretation = (
        "Significant (p < 0.01)"
    )

elif spearman_p < 0.05:

    spearman_interpretation = (
        "Significant (p < 0.05)"
    )

else:

    spearman_interpretation = (
        "Not significant (p >= 0.05)"
    )


print(
    f"Interpretation: "
    f"{spearman_interpretation}"
)


# ============================================================
# 4. GLYT2 : GEPHYRIN RATIO
# ============================================================

print()
print("============================================================")
print("4. GLYT2 : GEPHYRIN RATIO")
print("============================================================")


paired_df['GlyT2_Gephyrin_ratio'] = np.where(

    paired_df['Gephyrin_synapse_count'] > 0,

    paired_df['GlyT2_synapse_count']
    /
    paired_df['Gephyrin_synapse_count'],

    np.nan

)


ratio_mean = (
    paired_df['GlyT2_Gephyrin_ratio'].mean()
)

ratio_median = (
    paired_df['GlyT2_Gephyrin_ratio'].median()
)


print(
    f"Mean GlyT2:Gephyrin ratio: "
    f"{ratio_mean:.3f}"
)

print(
    f"Median GlyT2:Gephyrin ratio: "
    f"{ratio_median:.3f}"
)


# ============================================================
# SAVE PAIRED NEURON DATA
# ============================================================

paired_output_path = os.path.join(

    output_folder,

    'paired_neuron_statistics.csv'

)


paired_df.to_csv(

    paired_output_path,

    index=False

)


print()
print(
    f"Saved: {paired_output_path}"
)


# ============================================================
# SAVE STATISTICAL TEST RESULTS
# ============================================================

statistical_results = pd.DataFrame({

    'Analysis': [

        'Wilcoxon signed-rank test',

        'Spearman correlation'

    ],

    'Comparison': [

        'GlyT2 vs Gephyrin',

        'GlyT2 vs Gephyrin'

    ],

    'N': [

        len(paired_df),

        len(paired_df)

    ],

    'Statistic': [

        round(
            wilcoxon_stat,
            4
        ),

        round(
            spearman_rho,
            4
        )

    ],

    'P-value': [

        wilcoxon_p,

        spearman_p

    ],

    'Interpretation': [

        wilcoxon_interpretation,

        spearman_interpretation

    ]

})


statistics_path = os.path.join(

    output_folder,

    'priority_statistical_tests.csv'

)


statistical_results.to_csv(

    statistics_path,

    index=False

)


print()
print(
    f"Saved: {statistics_path}"
)


# ============================================================
# FIGURE 1 â€” GLYT2 VS GEPHYRIN BOXPLOT
# ============================================================

fig, ax = plt.subplots(

    figsize=(8, 8)

)


box = ax.boxplot(

    [
        glyt2,
        geph
    ],

    labels=[

        'GlyT2\n(Presynaptic)',

        'Gephyrin\n(Postsynaptic)'

    ],

    patch_artist=True

)


box['boxes'][0].set_facecolor(
    'gold'
)

box['boxes'][1].set_facecolor(
    'cyan'
)


ax.set_ylabel(

    'Synapse Count per Neuron',

    fontsize=12

)


ax.set_title(

    'GlyT2 vs Gephyrin Synapse Counts\nTDP-43',

    fontsize=14

)


ax.text(

    0.5,

    0.95,

    f'Wilcoxon signed-rank test\n'
    f'n = {len(paired_df)}\n'
    f'p = {wilcoxon_p:.4e}',

    transform=ax.transAxes,

    ha='center',

    va='top',

    fontsize=11

)


plt.tight_layout()


boxplot_path = os.path.join(

    output_folder,

    'glyt2_vs_gephyrin.png'

)


plt.savefig(

    boxplot_path,

    dpi=300

)


plt.show()


print(
    f"Saved: {boxplot_path}"
)


# ============================================================
# FIGURE 2 â€” SPEARMAN CORRELATION
# ============================================================

fig, ax = plt.subplots(

    figsize=(8, 8)

)


ax.scatter(

    glyt2,

    geph,

    alpha=0.5,

    s=20

)


ax.set_xlabel(

    'GlyT2 Synapses per Neuron',

    fontsize=12

)


ax.set_ylabel(

    'Gephyrin Synapses per Neuron',

    fontsize=12

)


ax.set_title(

    'GlyT2 vs Gephyrin Synapse Counts\nTDP-43',

    fontsize=14

)


ax.text(

    0.05,

    0.95,

    f'Spearman Ï = {spearman_rho:.3f}\n'
    f'p = {spearman_p:.4e}',

    transform=ax.transAxes,

    ha='left',

    va='top',

    fontsize=11

)


plt.tight_layout()


correlation_path = os.path.join(

    output_folder,

    'glyt2_gephyrin_correlation.png'

)


plt.savefig(

    correlation_path,

    dpi=300

)


plt.show()


print(
    f"Saved: {correlation_path}"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("============================================================")
print("PRIORITY STATISTICS COMPLETE")
print("============================================================")

print()

print(
    f"Paired neurons: "
    f"{len(paired_df)}"
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

print(
    "All results saved to:"
)

print(
    output_folder
)