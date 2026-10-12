import os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy import stats

src = sys.argv[1]   # repo results/statistics/paired_neuron_statistics.csv
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

# Crop region used for synapse detection (from crop_00.py / crop_01.py)
X0, Y0, W, H = 6588, 252, 4992, 7740

BLUE, ORANGE, GRAY = "#2a78d6", "#eb6834", "#b9b8b2"
INK, INK2, GRID, SURF = "#1a1a19", "#5f5e58", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "font.size": 11,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
})

d = pd.read_csv(src)
d["inside"] = d.neuron_x.between(X0, X0 + W, inclusive="left") & d.neuron_y.between(Y0, Y0 + H, inclusive="left")
ins = d[d.inside].copy()
G, P = "GlyT2_synapse_count", "Gephyrin_synapse_count"


def summary(df):
    g, p = df[G], df[P]
    r = (g / p.where(p > 0)).dropna()
    return {
        "Neuron entries (slice cross-sections)": len(df),
        "Total GlyT2 dots": int(g.sum()),
        "Total Gephyrin dots": int(p.sum()),
        "Mean GlyT2 per neuron": round(g.mean(), 2),
        "Mean Gephyrin per neuron": round(p.mean(), 2),
        "Median GlyT2 per neuron": float(g.median()),
        "Median Gephyrin per neuron": float(p.median()),
        "GlyT2 IQR (25th-75th)": f"{g.quantile(.25):.0f}-{g.quantile(.75):.0f}",
        "Gephyrin IQR (25th-75th)": f"{p.quantile(.25):.0f}-{p.quantile(.75):.0f}",
        "% with zero GlyT2": round((g == 0).mean() * 100, 1),
        "% with zero Gephyrin": round((p == 0).mean() * 100, 1),
        "% with zero of both": round(((g == 0) & (p == 0)).mean() * 100, 1),
        "Median GlyT2:Gephyrin ratio": round(r.median(), 3),
        "Total GlyT2 / total Gephyrin": round(g.sum() / p.sum(), 3),
        "Mean GlyT2:Gephyrin ratio (skewed, not recommended)": round(r.mean(), 3),
    }


s = pd.DataFrame({"All neurons (original)": summary(d), "Inside analyzed region (corrected)": summary(ins)})
s.index.name = "Measure"
s.to_csv(os.path.join(out, "corrected_summary.csv"))

rows = []
for label, df in [("All neurons (original)", d), ("Inside analyzed region (corrected)", ins)]:
    w = stats.wilcoxon(df[G], df[P])
    sp = stats.spearmanr(df[G], df[P])
    rows.append([label, "Wilcoxon signed-rank, GlyT2 vs Gephyrin", len(df), w.statistic, w.pvalue])
    rows.append([label, "Spearman correlation, GlyT2 vs Gephyrin", len(df), round(sp.statistic, 4), sp.pvalue])
t = pd.DataFrame(rows, columns=["Dataset", "Test", "N", "Statistic", "P-value"])
t["Note"] = "Neuron entries are 2D cross-sections; the same cell appears in several slices, so p-values are optimistic"
t.to_csv(os.path.join(out, "corrected_tests.csv"), index=False)

ins.drop(columns="inside").to_csv(os.path.join(out, "corrected_neuron_data.csv"), index=False)
byz = ins.groupby("Z_slice").agg(Number_of_neurons=(G, "size"),
                                 GlyT2_mean=(G, "mean"), GlyT2_median=(G, "median"), GlyT2_total=(G, "sum"),
                                 Gephyrin_mean=(P, "mean"), Gephyrin_median=(P, "median"), Gephyrin_total=(P, "sum")).round(2)
byz.to_csv(os.path.join(out, "corrected_by_Z_slice.csv"))

# 1. Where the neurons are vs where synapses were detected
fig, ax = plt.subplots(figsize=(7, 8))
out_df = d[~d.inside]
ax.scatter(out_df.neuron_x, out_df.neuron_y, s=1, c=GRAY, alpha=.25, lw=0, rasterized=True)
ax.scatter(ins.neuron_x, ins.neuron_y, s=1, c=BLUE, alpha=.25, lw=0, rasterized=True)
ax.add_patch(Rectangle((X0, Y0), W, H, fill=False, ec=INK, lw=1.5, ls="--"))
ax.text(X0 + 80, Y0 + 300, "Region where synapses\nwere detected (crop)", fontsize=10, va="top", color=INK)
ax.invert_yaxis(); ax.set_aspect("equal"); ax.grid(False)
ax.set_xlabel("X (pixels)"); ax.set_ylabel("Y (pixels)")
ax.set_title(f"Neuron positions, all slices combined\n{len(ins)/len(d):.0%} inside the analyzed region (blue), {len(out_df)/len(d):.0%} outside (gray)")
fig.tight_layout(); fig.savefig(os.path.join(out, "1_neuron_positions_vs_crop.png"), dpi=200); plt.close(fig)

# 2. Zero counts before vs after
labels = ["Zero GlyT2", "Zero Gephyrin", "Zero of both"]
a = [s.loc["% with zero GlyT2"].iloc[0], s.loc["% with zero Gephyrin"].iloc[0], s.loc["% with zero of both"].iloc[0]]
b = [s.loc["% with zero GlyT2"].iloc[1], s.loc["% with zero Gephyrin"].iloc[1], s.loc["% with zero of both"].iloc[1]]
x = np.arange(3); wbar = .36
fig, ax = plt.subplots(figsize=(8, 4.8))
b1 = ax.bar(x - wbar/2 - .01, a, wbar, color=GRAY, label="All neurons (original)")
b2 = ax.bar(x + wbar/2 + .01, b, wbar, color=BLUE, label="Inside analyzed region")
for bars in (b1, b2):
    for r in bars:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 1.2, f"{r.get_height():.0f}%", ha="center", fontsize=10, color=INK)
ax.set_xticks(x, labels); ax.set_ylim(0, 100); ax.set_ylabel("% of neuron entries"); ax.grid(axis="x", visible=False)
ax.legend(frameon=False, loc="upper right")
ax.set_title("Most zeros came from neurons outside the analyzed region")
fig.tight_layout(); fig.savefig(os.path.join(out, "2_zero_counts_before_after.png"), dpi=200); plt.close(fig)

# 3. GlyT2 vs Gephyrin per neuron, inside region
cap = np.percentile(np.r_[ins[G], ins[P]], 99)
fig, ax = plt.subplots(figsize=(6.5, 5.5))
bp = ax.boxplot([ins[G], ins[P]], widths=.5, patch_artist=True, showfliers=False,
                medianprops=dict(color=INK, lw=2), whiskerprops=dict(color=INK2), capprops=dict(color=INK2))
for patch, c in zip(bp["boxes"], [BLUE, ORANGE]):
    patch.set_facecolor(c); patch.set_alpha(.85); patch.set_edgecolor(c)
ax.set_xticks([1, 2], ["GlyT2\n(presynaptic)", "Gephyrin\n(postsynaptic)"])
for i, col in enumerate([G, P], start=1):
    ax.text(i + .3, ins[col].median(), f"median {ins[col].median():.0f}", va="center", fontsize=10, color=INK)
ax.set_ylabel("Dots matched per neuron entry"); ax.grid(axis="x", visible=False)
ax.set_title(f"Synapse counts per neuron, inside analyzed region\n(n = {len(ins):,}; outliers hidden)")
fig.tight_layout(); fig.savefig(os.path.join(out, "3_glyt2_vs_gephyrin_corrected.png"), dpi=200); plt.close(fig)

# 4. Correlation, inside region
sp_in = stats.spearmanr(ins[G], ins[P]).statistic
sp_all = stats.spearmanr(d[G], d[P]).statistic
fig, ax = plt.subplots(figsize=(6.5, 5.5))
lim = np.percentile(np.r_[ins[G], ins[P]], 99)
hb = ax.hexbin(ins[G].clip(upper=lim), ins[P].clip(upper=lim), gridsize=45, cmap="Blues", mincnt=1, bins="log", lw=0)
fig.colorbar(hb, ax=ax, label="Neuron entries (log scale)")
ax.set_xlabel("GlyT2 dots per neuron (top 1% shown at the edge)"); ax.set_ylabel("Gephyrin dots per neuron (top 1% at edge)"); ax.grid(False)
ax.set_title(f"GlyT2 vs Gephyrin, inside analyzed region\nSpearman = {sp_in:.2f} (was {sp_all:.2f} with all neurons)")
fig.tight_layout(); fig.savefig(os.path.join(out, "4_correlation_corrected.png"), dpi=200); plt.close(fig)

# 5. Across depth, inside region
roll = byz[["GlyT2_median", "Gephyrin_median"]].rolling(15, center=True, min_periods=5).mean()
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(roll.index, roll.GlyT2_median, color=BLUE, lw=2, label="GlyT2")
ax.plot(roll.index, roll.Gephyrin_median, color=ORANGE, lw=2, label="Gephyrin")
ax.set_ylim(0, 200); ax.set_xlim(0, 930)
ax.axvspan(840, 921, color=GRAY, alpha=.25, lw=0)
ax.annotate("Slices ~840-921: Gephyrin drops to 0,\nthen jumps to ~1,000-2,150 per neuron\n(off the chart). Likely an image problem.",
            xy=(845, 195), xytext=(560, 185), fontsize=9, color=INK, va="top",
            arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
ax.legend(frameon=False, loc="upper left")
ax.set_xlabel("Z slice (3 µm apart)"); ax.set_ylabel("Median dots per neuron")
ax.set_title("Synapse counts across tissue depth, inside analyzed region\n(15-slice rolling average)")
fig.tight_layout(); fig.savefig(os.path.join(out, "5_counts_by_depth_corrected.png"), dpi=200); plt.close(fig)

print("Saved to", out)
print(s.to_string())
print(t[["Dataset", "Test", "N", "Statistic", "P-value"]].to_string())
