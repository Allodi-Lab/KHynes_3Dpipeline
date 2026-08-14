import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

output_folder = r"D:\Conn_3dpipeline\results\statistics"
os.makedirs(output_folder, exist_ok=True)

# Load results
glyt2_path = r"D:\Conn_3dpipeline\results\matching\TDP43_synapse_counts.csv"
geph_path = r"D:\Conn_3dpipeline\results\matching\TDP43_gephyrin_counts.csv"

glyt2_df = pd.read_csv(glyt2_path)
geph_df = pd.read_csv(geph_path)

print(f"GlyT2 — Total neurons: {len(glyt2_df)}")
print(f"GlyT2 — Mean synapses per neuron: {glyt2_df['GlyT2_synapse_count'].mean():.2f}")
print(f"GlyT2 — Median synapses per neuron: {glyt2_df['GlyT2_synapse_count'].median():.2f}")
print(f"GlyT2 — Std: {glyt2_df['GlyT2_synapse_count'].std():.2f}")
print()
print(f"Gephyrin — Total neurons: {len(geph_df)}")
print(f"Gephyrin — Mean synapses per neuron: {geph_df['Gephyrin_synapse_count'].mean():.2f}")
print(f"Gephyrin — Median synapses per neuron: {geph_df['Gephyrin_synapse_count'].median():.2f}")
print(f"Gephyrin — Std: {geph_df['Gephyrin_synapse_count'].std():.2f}")

# ============================================================
# Figure 1 — Distribution of synapse counts per neuron
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].hist(glyt2_df['GlyT2_synapse_count'], bins=50, 
             color='gold', edgecolor='black', alpha=0.8)
axes[0].set_xlabel('GlyT2 Synapses per Neuron', fontsize=12)
axes[0].set_ylabel('Number of Neurons', fontsize=12)
axes[0].set_title('Distribution of GlyT2 Synapse Counts\nTDP-43', fontsize=13)
axes[0].axvline(glyt2_df['GlyT2_synapse_count'].mean(), 
                color='red', linestyle='--', label=f"Mean: {glyt2_df['GlyT2_synapse_count'].mean():.1f}")
axes[0].legend()

axes[1].hist(geph_df['Gephyrin_synapse_count'], bins=50,
             color='cyan', edgecolor='black', alpha=0.8)
axes[1].set_xlabel('Gephyrin Synapses per Neuron', fontsize=12)
axes[1].set_ylabel('Number of Neurons', fontsize=12)
axes[1].set_title('Distribution of Gephyrin Synapse Counts\nTDP-43', fontsize=13)
axes[1].axvline(geph_df['Gephyrin_synapse_count'].mean(),
                color='red', linestyle='--', label=f"Mean: {geph_df['Gephyrin_synapse_count'].mean():.1f}")
axes[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'synapse_distributions.png'), dpi=150)
plt.show()
print("Saved synapse_distributions.png")

# ============================================================
# Figure 2 — Per slice synapse counts
# ============================================================
glyt2_per_slice = glyt2_df.groupby('Z_slice')['GlyT2_synapse_count'].mean()
geph_per_slice = geph_df.groupby('Z_slice')['Gephyrin_synapse_count'].mean()

fig, axes = plt.subplots(2, 1, figsize=(16, 10))

axes[0].plot(glyt2_per_slice.index, glyt2_per_slice.values, 
             color='gold', linewidth=1.5, alpha=0.8)
axes[0].fill_between(glyt2_per_slice.index, glyt2_per_slice.values, 
                      alpha=0.3, color='gold')
axes[0].set_xlabel('Z Slice', fontsize=12)
axes[0].set_ylabel('Mean GlyT2 Synapses\nper Neuron', fontsize=12)
axes[0].set_title('GlyT2 Synapse Count Through Tissue Depth — TDP-43', fontsize=13)

axes[1].plot(geph_per_slice.index, geph_per_slice.values,
             color='cyan', linewidth=1.5, alpha=0.8)
axes[1].fill_between(geph_per_slice.index, geph_per_slice.values,
                      alpha=0.3, color='cyan')
axes[1].set_xlabel('Z Slice', fontsize=12)
axes[1].set_ylabel('Mean Gephyrin Synapses\nper Neuron', fontsize=12)
axes[1].set_title('Gephyrin Synapse Count Through Tissue Depth — TDP-43', fontsize=13)

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'synapse_per_slice.png'), dpi=150)
plt.show()
print("Saved synapse_per_slice.png")

# ============================================================
# Figure 3 — Box plot comparison GlyT2 vs Gephyrin
# ============================================================
fig, ax = plt.subplots(figsize=(8, 8))

data = [glyt2_df['GlyT2_synapse_count'].values,
        geph_df['Gephyrin_synapse_count'].values]

bp = ax.boxplot(data, labels=['GlyT2\n(Presynaptic)', 'Gephyrin\n(Postsynaptic)'],
                patch_artist=True, notch=False)

bp['boxes'][0].set_facecolor('gold')
bp['boxes'][1].set_facecolor('cyan')

ax.set_ylabel('Synapse Count per Neuron', fontsize=12)
ax.set_title('GlyT2 vs Gephyrin Synapse Counts\nTDP-43', fontsize=13)

# Statistical test
stat, p = stats.mannwhitneyu(glyt2_df['GlyT2_synapse_count'],
                              geph_df['Gephyrin_synapse_count'])
ax.text(0.5, 0.95, f'Mann-Whitney U test\np = {p:.4f}',
        transform=ax.transAxes, ha='center', va='top', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'glyt2_vs_gephyrin_boxplot.png'), dpi=150)
plt.show()
print("Saved glyt2_vs_gephyrin_boxplot.png")

# ============================================================
# Save summary statistics
# ============================================================
summary = {
    'Metric': ['Total Neurons', 'Mean Synapses/Neuron', 
                'Median Synapses/Neuron', 'Std', 'Total Synapses'],
    'GlyT2 (Presynaptic)': [
        len(glyt2_df),
        round(glyt2_df['GlyT2_synapse_count'].mean(), 2),
        round(glyt2_df['GlyT2_synapse_count'].median(), 2),
        round(glyt2_df['GlyT2_synapse_count'].std(), 2),
        glyt2_df['GlyT2_synapse_count'].sum()
    ],
    'Gephyrin (Postsynaptic)': [
        len(geph_df),
        round(geph_df['Gephyrin_synapse_count'].mean(), 2),
        round(geph_df['Gephyrin_synapse_count'].median(), 2),
        round(geph_df['Gephyrin_synapse_count'].std(), 2),
        geph_df['Gephyrin_synapse_count'].sum()
    ]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv(os.path.join(output_folder, 'summary_statistics.csv'), index=False)
print("\nSummary Statistics:")
print(summary_df.to_string(index=False))
print("\nSaved summary_statistics.csv")