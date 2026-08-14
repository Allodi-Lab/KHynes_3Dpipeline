# KHynes 3D Synapse Analysis Pipeline

## Overview

This repository contains the computational pipeline developed for quantitative analysis of 3D light-sheet microscopy data from the hTDP-43 mouse model.

The purpose of the project was to develop a reproducible 3D image-analysis workflow for quantifying glycinergic synaptic inputs at the level of individual neurons.

The pipeline processes microscopy images, detects synaptic puncta, identifies individual neurons using segmentation masks, assigns detected synapses to individual neurons, and performs statistical analysis of the resulting per-neuron measurements.

Two synaptic markers were analysed:

- **GlyT2** — presynaptic glycinergic synaptic marker
- **Gephyrin** — postsynaptic inhibitory synaptic marker

Neuron segmentation masks were used to associate detected synaptic puncta with individual neurons.

---

# Project Aim

The overall aim was to develop a 3D computational pipeline capable of converting large-scale microscopy data into quantitative measurements of synaptic input at the individual-neuron level.

The pipeline was designed to:

1. Prepare and process 3D microscopy data.
2. Separate and analyse individual fluorescence channels.
3. Detect GlyT2 and Gephyrin synaptic puncta.
4. Process neuron segmentation masks.
5. Identify individual neurons.
6. Match detected synapses to individual neurons.
7. Calculate synapse counts for each neuron.
8. Compare GlyT2 and Gephyrin measurements.
9. Examine the relationship between presynaptic and postsynaptic markers.
10. Generate visualisations for quality control.
11. Produce summary statistics for downstream analysis.

---

# Data and Imaging Channels

The microscopy dataset consisted of 3D light-sheet microscopy data acquired from the hTDP-43 mouse model.

The relevant channels used during analysis were:

| Channel | Marker | Purpose |
|---|---|---|
| C00 | GlyT2 | Presynaptic glycinergic synapses |
| C01 | Gephyrin | Postsynaptic inhibitory synapses |
| C02 | Neuron segmentation masks | Identification of individual neurons |

The GlyT2 and Gephyrin analyses used the same underlying set of segmented neurons, allowing paired comparisons between the two measurements.

---

# Environment Setup

The analysis was developed using a Conda environment named:

```text
cellpose2
````

## 1. Activate the Conda environment

Open **Anaconda Prompt** or another terminal where Conda is available.

Run:

```bash
conda activate cellpose2
```

The environment should be activated before running the Python scripts.

## 2. Verify Python

After activating the environment, Python can be checked using:

```bash
python --version
```

## 3. Required Python packages

The pipeline uses several Python libraries, including:

* NumPy
* Pandas
* Matplotlib
* SciPy
* scikit-image
* tifffile
* Cellpose

Additional dependencies may be required by individual scripts.

---

# Project Directory

The original pipeline was developed using the following Windows directory:

```text
D:\Conn_3dpipeline
```

The main project structure is:

```text
KHynes_3Dpipeline/
│
├── README.md
│
├── notebooks/
│   ├── Python analysis scripts
│   ├── Image preparation
│   ├── Synapse detection
│   ├── Neuron processing
│   ├── Synapse-neuron matching
│   ├── Visualisation
│   └── Statistical analysis
│
└── results/
    │
    ├── matching/
    ├── neuron_measurements/
    ├── statistics/
    └── visualizations/
```

The directory named `notebooks` contains Python scripts developed throughout the project. The name is retained from the original project structure even though most files are `.py` scripts rather than Jupyter notebooks.

---

# Quick Start

## Step 1 — Activate the environment

```bash
conda activate cellpose2
```

## Step 2 — Navigate to the project directory

```bash
cd D:\Conn_3dpipeline
```

## Step 3 — Prepare the microscopy data

Run the appropriate image conversion and preparation scripts located in:

```text
notebooks/
```

Relevant scripts include:

```text
convert_C00.py
convert_C01.py
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
crop_00.py
crop_01.py
crop_02.py
crop_WT_C01.py
```

Image alignment and volume checks can be performed using:

```text
check_alignment.py
check_volume.py
```

---

# Pipeline Workflow

The complete analysis workflow was:

```text
3D microscopy data
        |
        v
Channel conversion
        |
        v
Image cropping and preparation
        |
        v
Channel alignment / quality control
        |
        v
Synapse detection
        |
        v
Neuron segmentation masks
        |
        v
Synapse-to-neuron matching
        |
        v
Per-neuron GlyT2 and Gephyrin counts
        |
        v
Visualisation / quality control
        |
        v
Statistical analysis
        |
        v
Final quantitative results
```

---

# 1. Image Conversion and Preparation

The first stage involved preparing the microscopy data for downstream analysis.

Individual fluorescence channels were converted and prepared for analysis.

Relevant scripts include:

```text
convert_C00.py
convert_C01.py
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
```

Images were then cropped to the regions required for analysis.

Relevant scripts include:

```text
crop_00.py
crop_01.py
crop_02.py
crop_WT_C01.py
```

Alignment and image-volume checks were performed using:

```text
check_alignment.py
check_volume.py
```

These steps ensured that the relevant image channels were spatially compatible before synapse detection and neuron matching.

---

# 2. Synapse Detection

Synaptic puncta were detected separately in the GlyT2 and Gephyrin channels.

GlyT2 was treated as a marker of presynaptic glycinergic terminals, while Gephyrin was used as a marker of postsynaptic inhibitory synaptic specialisations.

Relevant scripts include:

```text
detect_synapse.py
detect_synapse_C01.py
detect_synapses.py
synquant_batch.py
synquant_batch.ijm
```

SynQuant was used as part of the synapse-detection workflow.

The detection process produced coordinate-based information for detected synaptic puncta.

These coordinates were subsequently used during the neuron-matching stage.

---

# 3. Neuron Segmentation

Individual neurons were represented using labelled segmentation masks.

Each non-zero label in the mask corresponded to an individual neuron.

The segmentation workflow was used to identify:

* Individual neuron IDs
* Neuron centroid X coordinates
* Neuron centroid Y coordinates
* Neuron locations within the image

Relevant scripts include:

```text
stack_masks.py
stack_masks_WT.py
neuron_measurement.py
visualize_neurons.py
```

The segmentation masks provided the spatial reference required to associate synaptic puncta with individual neurons.

---

# 4. Synapse-to-Neuron Matching

The synapse-to-neuron matching stage linked detected synaptic puncta to individual segmented neurons.

This was a key step in the pipeline because synapse detection initially produces a set of detected puncta but does not directly provide a neuron-level measurement.

The matching workflow:

1. Loaded the neuron segmentation mask.
2. Identified individual neuron labels.
3. Loaded detected synapse coordinates.
4. Compared synapse locations with the neuron segmentation.
5. Assigned detected synapses to neurons according to their spatial relationship.
6. Counted the matched synapses for each neuron.
7. Saved the resulting per-neuron measurements.

Relevant scripts include:

```text
match_synapse.py
match_synapse_C01.py
match_synapses.py
```

The process was performed independently for GlyT2 and Gephyrin.

---

# 5. Per-Neuron Data

The final matching datasets contain one row for each neuron and include information about its location and associated synapse count.

The GlyT2 dataset contains:

```text
Z_slice
neuron_id
neuron_x
neuron_y
GlyT2_synapse_count
```

The Gephyrin dataset contains:

```text
Z_slice
neuron_id
neuron_x
neuron_y
Gephyrin_synapse_count
```

These files are stored in:

```text
results/matching/
```

The same neuron set was used for both measurements, allowing paired statistical analysis.

---

# 6. Neuron Measurements

Additional measurements were calculated from the neuron segmentation masks.

These measurements provide quantitative information about the segmented neurons and provide a basis for future analysis of relationships between neuronal size and synaptic input.

The corresponding script is:

```text
neuron_measurement.py
```

Results are stored in:

```text
results/neuron_measurements/
```

---

# 7. Visualisation and Quality Control

Visualisation was used throughout the pipeline to verify image processing, synapse detection, neuron segmentation, and neuron-synapse matching.

Relevant scripts include:

```text
visualize_all_channels.py
visualize_detections.py
visualize_detections_01.py
visualize_neurons.py
visualize_matching.py
visualize_matching2.py
visualization_matching.py
visualize_overlay.py
animate_slices.py
make_slice_gif.py
make_3d_volume_gif.py
mask_3d_gif.py
```

These scripts produced visual outputs showing:

* Individual image channels
* Detected synaptic puncta
* Neuron segmentation
* Synapse-neuron spatial relationships
* Synapse counts associated with individual neurons
* 3D image volumes and masks

The resulting figures are stored in:

```text
results/visualizations/
```

---

# 8. Statistical Analysis

Statistical analysis was performed using the final per-neuron GlyT2 and Gephyrin datasets.

The analysis included descriptive statistics, distributions, slice-level analysis, paired comparisons, and correlation analysis.

Relevant scripts include:

```text
statistics.py
stats_2.py
all_stats.py
final_analysis.py
```

Statistical outputs are stored in:

```text
results/statistics/
```

## Descriptive Statistics

The following measurements were calculated:

* Total number of paired neurons
* Total GlyT2 synapses
* Total Gephyrin synapses
* Mean synapses per neuron
* Median synapses per neuron
* Standard deviation
* Minimum synapse count
* Maximum synapse count

## Distribution Analysis

The distribution of synapse counts across neurons was visualised using histograms.

These plots were used to assess the distribution and variability of synaptic input across individual neurons.

## Z-Slice Analysis

Synapse counts were also summarised by Z slice.

This allowed the distribution of synaptic measurements through the analysed tissue depth to be examined.

## GlyT2 vs Gephyrin Comparison

Because GlyT2 and Gephyrin measurements were obtained from the same set of neurons, a paired statistical comparison was performed using the **Wilcoxon signed-rank test**.

## GlyT2–Gephyrin Correlation

The relationship between GlyT2 and Gephyrin synapse counts across individual neurons was assessed using **Spearman's rank correlation coefficient**.

---

# Final Results

The final analysis included:

**79,460 paired neurons**

The total matched synapse counts were:

| Measurement                      |    Result |
| -------------------------------- | --------: |
| Paired neurons                   |    79,460 |
| Total GlyT2 synapses             |   993,397 |
| Total Gephyrin synapses          | 1,161,821 |
| Mean GlyT2 synapses/neuron       |    12.502 |
| Mean Gephyrin synapses/neuron    |    14.621 |
| Median GlyT2 synapses/neuron     |         0 |
| Median Gephyrin synapses/neuron  |         0 |
| GlyT2 standard deviation         |    41.577 |
| Gephyrin standard deviation      |    41.035 |
| Minimum GlyT2 synapses/neuron    |         0 |
| Minimum Gephyrin synapses/neuron |         0 |
| Maximum GlyT2 synapses/neuron    |       609 |
| Maximum Gephyrin synapses/neuron |     2,154 |

---

# Statistical Results

## Wilcoxon Signed-Rank Test

The paired comparison between GlyT2 and Gephyrin synapse counts produced:

```text
Wilcoxon statistic = 119,574,968
p = 3.15 × 10^-203
```

This indicates a statistically significant difference between the paired GlyT2 and Gephyrin measurements.

## Spearman Correlation

The correlation between GlyT2 and Gephyrin synapse counts was:

```text
Spearman rho = 0.7217
p < 0.001
```

This indicates a strong positive association between GlyT2 and Gephyrin synapse counts across individual neurons.

Because the analysis contains a very large number of observations, statistical significance should be interpreted alongside the magnitude of the observed association and its biological relevance.

---

# Results Directory

The generated outputs are organised into four main directories.

## `results/matching/`

Contains per-neuron synapse matching results, including:

```text
TDP43_synapse_counts.csv
TDP43_gephyrin_counts.csv
```

These datasets contain the final neuron-level GlyT2 and Gephyrin measurements.

## `results/neuron_measurements/`

Contains quantitative measurements derived from the neuron segmentation masks.

## `results/statistics/`

Contains statistical summaries, tables, and analysis outputs.

## `results/visualizations/`

Contains figures generated during image processing, quality control, matching, and statistical analysis.

---

# Running Individual Scripts

Once the Conda environment is activated:

```bash
conda activate cellpose2
```

Navigate to the project directory:

```bash
cd D:\Conn_3dpipeline
```

Individual scripts can then be executed using:

```bash
python script_name.py
```

For example:

```bash
python final_analysis.py
```

Individual scripts may contain file paths specific to the original analysis environment.

These paths may need to be changed when running the pipeline on another computer or dataset.

---

# Important Notes

## Raw Microscopy Data

The original microscopy datasets are not included in this repository because of their large file sizes.

The scripts therefore require the user to provide their own local paths to the original image data.

## File Paths

The original analysis used Windows paths beginning with:

```text
D:\Conn_3dpipeline
```

When transferring the pipeline to another computer, file paths inside the scripts should be updated accordingly.

## Reproducibility

The repository contains the Python analysis scripts and generated results used during development of the pipeline.

The complete conceptual workflow is:

```text
Microscopy data
      ↓
Channel conversion
      ↓
Cropping and preparation
      ↓
Alignment / QC
      ↓
Synapse detection
      ↓
Neuron segmentation
      ↓
Synapse-neuron matching
      ↓
Per-neuron quantification
      ↓
Statistical analysis
      ↓
Visualisation
```

This structure allows individual stages of the analysis to be inspected, modified, or rerun independently.

---

# Future Development

The pipeline provides a foundation for further quantitative analysis of 3D neuronal and synaptic organisation.

Potential future extensions include:

* Normalising synapse counts by neuron size
* Incorporating additional neuronal morphological measurements
* Comparing experimental groups
* Extending the analysis to additional brain regions
* Analysing synaptic distributions in full 3D volumes
* Automating parameter selection for synapse detection
* Improving neuron-synapse assignment methods
* Extending the pipeline to additional synaptic markers

---

# Summary

This project developed a computational workflow for analysing 3D light-sheet microscopy data at the individual-neuron level.

The pipeline integrates:

* Image processing
* Channel preparation
* Synapse detection
* Neuron segmentation
* Synapse-neuron matching
* Per-neuron quantification
* Visual quality control
* Statistical analysis

The final analysis quantified GlyT2 and Gephyrin synaptic inputs across **79,460 paired neurons**, providing a large-scale quantitative dataset for investigating glycinergic synaptic organisation in the hTDP-43 mouse model.

---

# Author

**K. Hynes**

University of St Andrews
School of Neuroscience

## Repository

[KHynes 3D Pipeline](https://github.com/Allodi-Lab/KHynes_3Dpipeline)

```

**That is the one to paste into `README.md` on GitHub.**
```
