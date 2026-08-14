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

glyt2_path = r"D:\Conn_3dpipeline\results\matching\TDP43_synapse_counts.csv"

geph_path = r"D:\Conn_3dpipeline\results\matching\TDP43_gephyrin_counts.csv"


# ============================================================
# LOAD RESULTS
# ============================================================

print("Loading matching results...")

glyt2_df = pd.read_csv(glyt2_path)

geph_df = pd.read_csv(geph_path)


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

glyt2_df = glyt2_df.copy()

geph_df = geph_df.copy()


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
glyt2_df['GlyT2_synapse_count'] = pd.to_numeric(
    glyt2_df['GlyT2_synapse_count'],
    errors='coerce'
)

geph_df['Gephyrin_synapse_count'] = pd.to_numeric(
    geph_df['Gephyrin_synapse_count'],
    errors='coerce'
)


# Remove incomplete rows
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


# Convert IDs to integers
glyt2_df['Z_slice'] = glyt2_df['Z_slice'].astype(int)

geph_df['Z_slice'] = geph_df['Z_slice'].astype(int)

glyt2_df['neuron_id'] = glyt2_df['neuron_id'].astype(int)

geph_df['neuron_id'] = geph_df['neuron_id'].astype(int)


# ============================================================
# BASIC SUMMARY
# ============================================================

print()
print("============================================================")
print("BASIC SUMMARY")
print("============================================================")

print(
    f"GlyT2 - Total neurons: "
    f"{len(glyt2_df)}"
)

print(
    f"GlyT2 - Mean synapses per neuron: "
    f"{glyt2_df['GlyT2_synapse_count'].mean():.2f}"
)

print(
    f"GlyT2 - Median synapses per neuron: "
    f"{glyt2_df['GlyT2_synapse_count'].median():.2f}"
)

print(
    f"GlyT2 - Standard Deviation: "
    f"{glyt2_df['GlyT2_synapse_count'].std():.2f}"
)

print(
    f"GlyT2 - Total synapses: "
    f"{glyt2_df['GlyT2_synapse_count'].sum()}"
)

print()

print(
    f"Gephyrin - Total neurons: "
    f"{len(geph_df)}"
)

print(
    f"Gephyrin - Mean synapses per neuron: "
    f"{geph_df['Gephyrin_synapse_count'].mean():.2f}"
)

print(
    f"Gephyrin - Median synapses per neuron: "
    f"{geph_df['Gephyrin_synapse_count'].median():.2f}"
)

print(
    f"Gephyrin - Std: "
    f"{geph_df['Gephyrin_synapse_count'].std():.2f}"
)

print(
    f"Gephyrin - Total synapses: "
    f"{geph_df['Gephyrin_synapse_count'].sum()}"
)


# ============================================================
# FIGURE 1
# DISTRIBUTION OF SYNAPSE COUNTS PER NEURON
# ============================================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(16, 6)
)


# ----------------------------
# GlyT2
# ----------------------------

glyt2_values = glyt2_df['GlyT2_synapse_count']

glyt2_mean = glyt2_values.mean()


axes[0].hist(
    glyt2_values,
    bins=50,
    color='gold',
    edgecolor='black',
    alpha=0.8
)

axes[0].axvline(
    glyt2_mean,
    color='red',
    linestyle='--',
    label=f'Mean: {glyt2_mean:.1f}'
)

axes[0].set_xlabel(
    'GlyT2 Synapses per Neuron',
    fontsize=12
)

axes[0].set_ylabel(
    'Number of Neurons',
    fontsize=12
)

axes[0].set_title(
    'Distribution of GlyT2 Synapse Counts\nTDP-43',
    fontsize=13
)

axes[0].legend()


# ----------------------------
# Gephyrin
# ----------------------------

geph_values = geph_df['Gephyrin_synapse_count']

geph_mean = geph_values.mean()


axes[1].hist(
    geph_values,
    bins=50,
    color='cyan',
    edgecolor='black',
    alpha=0.8
)

axes[1].axvline(
    geph_mean,
    color='red',
    linestyle='--',
    label=f'Mean: {geph_mean:.1f}'
)

axes[1].set_xlabel(
    'Gephyrin Synapses per Neuron',
    fontsize=12
)

axes[1].set_ylabel(
    'Number of Neurons',
    fontsize=12
)

axes[1].set_title(
    'Distribution of Gephyrin Synapse Counts\nTDP-43',
    fontsize=13
)

axes[1].legend()


plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        'synapse_distributions.png'
    ),
    dpi=150
)

plt.show()

print("\nSaved synapse_distributions.png")


# ============================================================
# FIGURE 2
# SYNAPSE COUNTS THROUGH TISSUE DEPTH
# ============================================================

glyt2_per_slice = (
    glyt2_df
    .groupby('Z_slice')['GlyT2_synapse_count']
    .mean()
    .sort_index()
)

geph_per_slice = (
    geph_df
    .groupby('Z_slice')['Gephyrin_synapse_count']
    .mean()
    .sort_index()
)


fig, axes = plt.subplots(
    2,
    1,
    figsize=(16, 10)
)


# ----------------------------
# GlyT2
# ----------------------------

axes[0].plot(
    glyt2_per_slice.index,
    glyt2_per_slice.values,
    color='gold',
    linewidth=1.5,
    alpha=0.8
)

axes[0].fill_between(
    glyt2_per_slice.index,
    glyt2_per_slice.values,
    alpha=0.3,
    color='gold'
)

axes[0].set_xlabel(
    'Z Slice',
    fontsize=12
)

axes[0].set_ylabel(
    'Mean GlyT2 Synapses\nper Neuron',
    fontsize=12
)

axes[0].set_title(
    'GlyT2 Synapse Count Through Tissue Depth - TDP-43',
    fontsize=13
)


# ----------------------------
# Gephyrin
# ----------------------------

axes[1].plot(
    geph_per_slice.index,
    geph_per_slice.values,
    color='cyan',
    linewidth=1.5,
    alpha=0.8
)

axes[1].fill_between(
    geph_per_slice.index,
    geph_per_slice.values,
    alpha=0.3,
    color='cyan'
)

axes[1].set_xlabel(
    'Z Slice',
    fontsize=12
)

axes[1].set_ylabel(
    'Mean Gephyrin Synapses\nper Neuron',
    fontsize=12
)

axes[1].set_title(
    'Gephyrin Synapse Count Through Tissue Depth - TDP-43',
    fontsize=13
)


plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        'synapse_per_slice.png'
    ),
    dpi=150
)

plt.show()

print("\nSaved synapse_per_slice.png")


# ============================================================
# MATCH GLYT2 AND GEPHYRIN BY NEURON
# ============================================================

paired_df = pd.merge(
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

    how='inner'
)


print()
print("============================================================")
print("PAIRED GLYT2 / GEPHYRIN DATA")
print("============================================================")

print(
    f"Neurons with both measurements: "
    f"{len(paired_df)}"
)


# ============================================================
# FIGURE 3
# GLYT2 VS GEPHYRIN BOX PLOT
# ============================================================

fig, ax = plt.subplots(
    figsize=(8, 8)
)


paired_glyt2 = paired_df[
    'GlyT2_synapse_count'
].values

paired_geph = paired_df[
    'Gephyrin_synapse_count'
].values


data = [
    paired_glyt2,
    paired_geph
]


bp = ax.boxplot(
    data,
    labels=[
        'GlyT2\n(Presynaptic)',
        'Gephyrin\n(Postsynaptic)'
    ],
    patch_artist=True,
    notch=False
)


bp['boxes'][0].set_facecolor('gold')

bp['boxes'][1].set_facecolor('cyan')


ax.set_ylabel(
    'Synapse Count per Neuron',
    fontsize=12
)

ax.set_title(
    'GlyT2 vs Gephyrin Synapse Counts\nTDP-43',
    fontsize=13
)


# ============================================================
# WILCOXON SIGNED-RANK TEST
# ============================================================

if len(paired_df) > 0:

    wilcoxon_stat, wilcoxon_p = stats.wilcoxon(
        paired_df['GlyT2_synapse_count'],
        paired_df['Gephyrin_synapse_count']
    )

else:

    wilcoxon_stat = np.nan
    wilcoxon_p = np.nan


ax.text(
    0.5,
    0.95,
    f'Wilcoxon signed-rank test\n'
    f'n = {len(paired_df)}\n'
    f'p = {wilcoxon_p:.4g}',

    transform=ax.transAxes,

    ha='center',
    va='top',

    fontsize=11,

    bbox=dict(
        boxstyle='round',
        facecolor='wheat',
        alpha=0.5
    )
)


plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        'glyt2_vs_gephyrin_boxplot.png'
    ),
    dpi=150
)

plt.show()

print(
    "\nSaved glyt2_vs_gephyrin_boxplot.png"
)


# ============================================================
# FIGURE 4
# GLYT2 VS GEPHYRIN CORRELATION
# ============================================================

if len(paired_df) > 1:

    spearman_rho, spearman_p = stats.spearmanr(
        paired_df['GlyT2_synapse_count'],
        paired_df['Gephyrin_synapse_count']
    )


    fig, ax = plt.subplots(
        figsize=(8, 8)
    )


    ax.scatter(
        paired_df['GlyT2_synapse_count'],
        paired_df['Gephyrin_synapse_count'],
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
        'Relationship Between GlyT2 and Gephyrin Synapse Counts',
        fontsize=13
    )


    ax.text(
        0.05,
        0.95,

        f'Spearman Ï = {spearman_rho:.3f}\n'
        f'p = {spearman_p:.4e}',

        transform=ax.transAxes,

        ha='left',
        va='top',

        fontsize=11,

        bbox=dict(
            boxstyle='round',
            facecolor='white',
            alpha=0.8
        )
    )


    plt.tight_layout()

    plt.savefig(
        os.path.join(
            output_folder,
            'glyt2_gephyrin_correlation.png'
        ),
        dpi=150
    )

    plt.show()

    print(
        "\nSaved glyt2_gephyrin_correlation.png"
    )

else:

    spearman_rho = np.nan
    spearman_p = np.nan


# ============================================================
# CLEAN SUMMARY CSV
# ============================================================

summary_df = pd.DataFrame({

    'Measure': [

        'Number of neurons',

        'Mean synapses per neuron',

        'Median synapses per neuron',

        'Standard deviation',

        'Total synapses'

    ],

    'GlyT2 (Presynaptic)': [

        len(glyt2_df),

        round(glyt2_mean, 2),

        round(glyt2_values.median(), 2),

        round(glyt2_values.std(), 2),

        int(glyt2_values.sum())

    ],

    'Gephyrin (Postsynaptic)': [

        len(geph_df),

        round(geph_mean, 2),

        round(geph_values.median(), 2),

        round(geph_values.std(), 2),

        int(geph_values.sum())

    ]
})


summary_path = os.path.join(
    output_folder,
    'summary_statistics.csv'
)


summary_df.to_csv(
    summary_path,
    index=False
)


print()
print("============================================================")
print("SUMMARY STATISTICS")
print("============================================================")

print(
    summary_df.to_string(
        index=False
    )
)

print(
    f"\nSaved: {summary_path}"
)


# ============================================================
# STATISTICAL TEST RESULTS CSV
# ============================================================

def significance_label(p):

    if p < 0.001:

        return 'Highly significant (p < 0.001)'

    elif p < 0.01:

        return 'Significant (p < 0.01)'

    elif p < 0.05:

        return 'Significant (p < 0.05)'

    else:

        return 'Not significant (p >= 0.05)'


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

        round(wilcoxon_stat, 4),

        round(spearman_rho, 4)

    ],

    'P-value': [

        wilcoxon_p,

        spearman_p

    ],

    'Interpretation': [

        significance_label(wilcoxon_p),

        significance_label(spearman_p)

    ]
})


statistics_path = os.path.join(
    output_folder,
    'statistical_tests.csv'
)


statistical_results.to_csv(
    statistics_path,
    index=False
)


print()
print("============================================================")
print("STATISTICAL TEST RESULTS")
print("============================================================")

print(
    statistical_results.to_string(
        index=False
    )
)

print(
    f"\nSaved: {statistics_path}"
)


# ============================================================
# SAVE PAIRED NEURON DATA
# ============================================================

paired_output = paired_df.sort_values(
    by=[
        'Z_slice',
        'neuron_id'
    ]
)


paired_path = os.path.join(
    output_folder,
    'paired_neuron_data.csv'
)


paired_output.to_csv(
    paired_path,
    index=False
)


print(
    f"\nSaved: {paired_path}"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("============================================================")
print("STATISTICS ANALYSIS COMPLETE")
print("============================================================")

print()
print("Files created:")

print("1. summary_statistics.csv")

print("2. statistical_tests.csv")

print("3. paired_neuron_data.csv")

print("4. synapse_distributions.png")

print("5. synapse_per_slice.png")

print("6. glyt2_vs_gephyrin_boxplot.png")

print("7. glyt2_gephyrin_correlation.png")

print()
print("All results saved to:")

print(output_folder)