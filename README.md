# hTDP-43: 3D Synapse Analysis Pipeline
### Allodi Lab, University of St Andrews

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1%20CUDA-orange)
![Cellpose](https://img.shields.io/badge/Cellpose-4.2.1-green)
![Institution](https://img.shields.io/badge/Allodi%20Lab-St%20Andrews-purple)
![Status](https://img.shields.io/badge/Status-TDP--43%20Complete%20%7C%20WT%20To%20Do-yellow)

---

## Overview

This repository holds a pipeline for counting synapses on motor neurons in 3D light-sheet microscopy images of the spinal cord from the hTDP-43 mouse model of ALS.

The pipeline finds motor neurons, finds synaptic dots for two markers, assigns each dot to its nearest neuron, and then summarizes the counts.

- **GlyT2** marks presynaptic glycinergic terminals (the sending side of an inhibitory synapse).
- **Gephyrin** marks postsynaptic sites (the receiving side).

It extends the 2D analysis in Mora et al. (2024) into 3D. The raw images and large intermediate files are not stored here because of their size.

> **Please read [Corrected results](#corrected-results) before using any numbers from this repository.** The original statistics in `results/statistics/` include a large number of neurons that were never checked for synapses, which changes the conclusions.

---

## Project status

| Part | Status |
|------|--------|
| hTDP-43 pipeline (segmentation, detection, matching, stats) | Done |
| Corrected statistics (neurons inside the analyzed region only) | Done, see `corrected/` |
| Linking 2D neuron outlines into 3D cells | To do |
| Edge-based synapse matching | To do |
| WT (wild-type) comparison | To do, starter scripts included |

---

## Repository structure

```text
KHynes_3Dpipeline/
├── notebooks/            All pipeline scripts (see Script guide below)
├── results/
│   ├── matching/            Synapse counts per neuron, per slice
│   ├── neuron_measurements/ Per-neuron measurements and matching summary
│   ├── statistics/          ORIGINAL stats and plots (all neurons, see note above)
│   └── visualizations/      Quality-check images
├── corrected/            CORRECTED stats and plots (use these)
├── progress_updates.txt  Running notes from the project
└── README.md
```

---

## Pipeline overview

```text
Light-sheet images (.ome.tif, one file per slice per channel)
        │
        ▼
Convert to standard .tif
        │
        ▼
Neuron segmentation on C02 (Cellpose, custom model, full image)
        │
        ▼
Crop C00 and C01 to the analyzed region
        │
        ▼
Synapse dot detection on C00 and C01 (blob_log)
        │
        ▼
Match each dot to the nearest neuron center (KD-tree, 300 px limit)
        │
        ▼
Per-neuron counts → statistics → plots
```

### Channels

| Channel | Marker | Used for |
|---------|--------|----------|
| C00 | GlyT2 (647 nm) | Presynaptic dots |
| C01 | Gephyrin (555 nm) | Postsynaptic dots |
| C02 | Neurofilament / NeuroTrace | Finding motor neuron cell bodies |

The file names list four dyes (NF-780, GlyT2-647, Gef-555, nf-488) but there are only three channels, so this mapping should be confirmed with Dr Allodi.

### Analyzed region (crop)

Synapse detection only covers this region of each slice, which was chosen to contain the ventral horn motor neurons.

| x | y | width | height |
|---|---|-------|--------|
| 6588 | 252 | 4992 | 7740 |

Dot positions are shifted back into full-image coordinates (x + 6588, y + 252) before matching.

---

## Step by step

### 1. Convert images

The raw `.ome.tif` files are converted to plain `.tif` so the Python tools can read them. One C02 file (Z0000) failed to convert and is noted in `progress_updates.txt`.

### 2. Segment neurons (Cellpose)

Motor neurons are found in the C02 channel with a custom Cellpose model fine-tuned from `cpsam_v2` on about 82 hand-labeled motor neurons.

| Setting | Value |
|---------|-------|
| Base model | cpsam_v2 |
| Diameter | 28 |
| Cellprob threshold | -1.0 |
| Flow threshold | 0.4 |
| Training epochs | 100 |

`batch_process.py` runs the model on every slice of the **full, uncropped** image. Each slice is segmented on its own, so neuron IDs are only meaningful within one slice.

### 3. Detect synapse dots

Dots are found with `skimage.feature.blob_log` on the cropped C00 and C01 images. Each slice is contrast-stretched to its own 2nd–98th percentile, shrunk to 50% for speed, and then the dot positions are scaled back up.

| Setting | Value |
|---------|-------|
| min_sigma / max_sigma | 1 / 5 |
| threshold | 0.05 |
| Resolution | 50% |

SynQuantVid in FIJI was tried first but was not used in the final pipeline. Those scripts are kept for reference.

### 4. Match dots to neurons

Each dot is assigned to the nearest neuron center in the same slice, as long as it is within 300 pixels. This gives a GlyT2 count and a Gephyrin count for every neuron in every slice.

### 5. Statistics

`final_analysis.py` pairs the GlyT2 and Gephyrin counts for each neuron and runs a Wilcoxon signed-rank test and a Spearman correlation. `neuron_measurement.py` adds neuron area and dot density.

---

## Script guide

Several scripts have similar names because of earlier versions. These are the ones that produced the results.

| Step | Script used | Older / unused version |
|------|-------------|------------------------|
| Convert | `convert_C00.py`, `convert_C01.py` | |
| Crop | `crop_00.py`, `crop_01.py`, `crop_02.py` | |
| Segment | `batch_process.py`, `stack_masks.py` | |
| Detect GlyT2 | `detect_synapse.py` | `detect_synapses.py` |
| Detect Gephyrin | `detect_synapse_C01.py` | |
| Match GlyT2 | `match_synapse.py` | `match_synapses.py` (reads old SynQuant output, no crop shift) |
| Match Gephyrin | `match_synapse_C01.py` | |
| Measure | `neuron_measurement.py` | |
| Stats | `final_analysis.py` | `statistics.py`, `stats_2.py`, `all_stats.py` |
| SynQuant | | `synquant_batch.py`, `synquant_batch.ijm` |
| WT starters | `convert_WT_C00/01/02.py`, `crop_WT_C01.py`, `batch_process_WT.py`, `stack_masks_WT.py` | |
| Checks and plots | `check_alignment.py`, `check_volume.py`, `visualize_*.py`, `*_gif.py`, `animate_slices.py` | |

The folders that `detect_synapse.py` and `detect_synapse_C01.py` write to are named `C00_synquant2` and `C01_synquant`, even though they hold blob_log results.

---

## Corrected results

### What was wrong

Neuron segmentation ran on the full image, but synapse detection only ran inside the cropped region. So about **77% of neuron entries sit outside the area where synapses were looked for**, and they show up with zero (or nearly zero) synapses. Including them made the median 0 and created a strong correlation that came mostly from shared zeros.

### What was done

`corrected/corrected_stats.py` takes `results/statistics/paired_neuron_statistics.csv` and keeps only the neuron entries whose center falls inside the crop region. Then it reruns the summary statistics, tests, and plots. It only needs that CSV, not the raw images.

```bash
python corrected_stats.py ../results/statistics/paired_neuron_statistics.csv output_folder
```

### Before and after

| Measure | All neurons (original) | Inside analyzed region (corrected) |
|---------|------------------------|------------------------------------|
| Neuron entries | 79,460 | 18,140 |
| Median GlyT2 per neuron | 0 | 21 |
| Median Gephyrin per neuron | 0 | 38 |
| Zero of both markers | 69% | 1% |
| Total GlyT2 ÷ total Gephyrin | 0.86 | 1.10 |
| Wilcoxon, GlyT2 vs Gephyrin | p ≈ 3 × 10⁻²⁰³ | p = 0.06 |
| Spearman correlation | 0.72 | 0.01 |

With only the neurons that were actually analyzed, GlyT2 and Gephyrin counts are not clearly different and are not correlated.

### Files in `corrected/`

| File | What it shows |
|------|---------------|
| `1_neuron_positions_vs_crop.png` | Where neurons were found vs. where synapses were detected |
| `2_zero_counts_before_after.png` | Share of neurons with zero synapses, before and after |
| `3_glyt2_vs_gephyrin_corrected.png` | GlyT2 vs Gephyrin counts per neuron |
| `4_correlation_corrected.png` | GlyT2 vs Gephyrin for each neuron entry |
| `5_counts_by_depth_corrected.png` | Median counts across Z slices |
| `corrected_summary.csv` | Summary stats, original vs corrected |
| `corrected_tests.csv` | Wilcoxon and Spearman results, original vs corrected |
| `corrected_neuron_data.csv` | The 18,140 neuron entries used |
| `corrected_by_Z_slice.csv` | Counts per Z slice |
| `corrected_stats.py` | Script that made all of the above |

---

## Known issues and next steps

These are still open, roughly in order of importance.

1. **Neurons are counted once per slice, not once per cell.** Slices are 3 µm apart and a motor neuron spans many slices, so one cell appears many times. About 55% of neuron outlines reappear in almost the same spot in the next slice. This makes the p-values look stronger than they should. Cellpose's `stitch_threshold` setting can link outlines across slices into 3D cells.
2. **The 300-pixel matching radius is very wide.** Dots are assigned to the nearest neuron center, not to dots touching the cell. One neuron in slices 868–871 received over 2,100 Gephyrin dots. Counting dots within a few pixels of each neuron's outline would be closer to "synapses on this neuron." The pixel size in microns is needed to choose a good distance.
3. **Slices ~840–921 look unreliable for Gephyrin.** Gephyrin counts drop to zero, then jump to 1,000–2,150 per neuron. This is likely an image problem at the end of the stack.
4. **Counts swing a lot with depth, and the two markers often move in opposite directions.** Real paired synapses should track each other. One possible cause is that each slice is contrast-stretched on its own, which can turn noise into "dots" in slices with few real ones. Checking detection against hand counts on a few slices would help.
5. **Cellpose finds objects across the whole tissue**, not just the ventral horn. Cropping the masks to the analyzed region before matching would fix the main issue at the source.
6. **The "100% match rate" in `matching_quality.csv` is not a real check.** It compares matched dots against matched dots.
7. **The mean GlyT2:Gephyrin ratio is skewed** by a few neurons with very high ratios. Use the median ratio or the ratio of totals instead.
8. **WT data has not been processed.** The starter scripts are ready once the data is available.

---

## Setup

The pipeline was run on a Windows workstation with an NVIDIA RTX A5000, using a conda environment called `cellpose2`.

```bash
conda create -n cellpose2 python=3.10
conda activate cellpose2
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install cellpose==4.2.1
pip install tifffile numpy pandas scipy matplotlib scikit-image imageio roifile jupyter pyimagej
```

If Cellpose crashes with an OpenMP error on Windows, run this first.

```bash
set KMP_DUPLICATE_LIB_OK=TRUE
```

Then run any script with `python script_name.py`. Most scripts have file paths written in for the lab workstation (`D:\Conn_3dpipeline\...`), so update those before running on another machine.

---

## Data not included

These folders live on the lab workstation and are too large for GitHub.

```text
raw/  raw_converted/  cropped/  masks/  models/  training/
```

The full stacked mask volume is about 333 GB (84 GB at 50% scale).

---

## Citation

```
K. Hynes, Allodi Lab, University of St Andrews, 2026
```

- Stringer, C., et al. (2021). Cellpose: a generalist algorithm for cellular segmentation. *Nature Methods*, 18(1), 100–106.
- van der Walt, S., et al. (2014). scikit-image: image processing in Python. *PeerJ*, 2, e453.
- Wang, Y., et al. (2020). SynQuant: An automatic tool to quantify synapses from microscopy images. *Bioinformatics*, 36(5), 1599–1606. (Tested, not used in the final pipeline.)

## Acknowledgements

Developed by K. Hynes in the Allodi Lab, University of St Andrews, under the supervision of Dr Ilary Allodi. Light-sheet data were acquired at the LSM3D Facility, University of Edinburgh. This work extends the 2D pipeline in Mora et al. (2024).
