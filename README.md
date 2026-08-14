# 3D Synapse Analysis Pipeline

## Overview

This repository contains a computational pipeline for analysing 3D light-sheet microscopy images from the hTDP-43 mouse model.

The project focuses on using image analysis to identify neurons and synaptic puncta within large 3D microscopy datasets. The pipeline then links detected synapses to individual neurons so that synaptic input can be measured at the neuron level.

Two synaptic markers are analysed:

- **GlyT2** — a marker of presynaptic glycinergic terminals
- **Gephyrin** — a marker of postsynaptic inhibitory synapses

Neuron segmentation masks are used to identify individual neurons and provide the spatial information needed to match detected synapses to those neurons.

The pipeline produces per-neuron GlyT2 and Gephyrin synapse counts, neuron measurements, visualisations for quality control, and statistical analyses of the resulting data.

---

## Project Aim

The aim of the project was to develop a reproducible computational workflow for analysing 3D microscopy data and quantifying glycinergic synaptic input at the level of individual neurons.

The pipeline was designed to:

1. Prepare 3D microscopy images for analysis.
2. Separate and process the relevant imaging channels.
3. Detect GlyT2 and Gephyrin synaptic puncta.
4. Process neuron segmentation masks.
5. Identify individual neurons.
6. Match detected synapses to individual neurons.
7. Calculate synapse counts for each neuron.
8. Measure properties of segmented neurons.
9. Visualise the results for quality control.
10. Perform statistical analysis of the resulting measurements.

---

# Data

The pipeline was developed using 3D light-sheet microscopy data from the hTDP-43 mouse model.

Three main imaging channels were used:

| Channel | Marker | Purpose |
|---|---|---|
| C00 | GlyT2 | Presynaptic glycinergic synapses |
| C01 | Gephyrin | Postsynaptic inhibitory synapses |
| C02 | Neuron segmentation masks | Identification of individual neurons |

The GlyT2 and Gephyrin measurements use the same set of segmented neurons. This allows the two synaptic measurements to be compared directly for individual neurons.

---

# Pipeline Overview

The overall workflow is:

```text
3D light-sheet microscopy data
              |
              v
      Channel preparation
              |
              v
       Image cropping
              |
              v
   Alignment and volume checks
              |
              v
       Synapse detection
              |
              v
      Neuron segmentation
              |
              v
    Synapse-neuron matching
              |
              v
     Per-neuron measurements
              |
              v
       Quality control
              |
              v
      Statistical analysis
````

---

# Environment Setup

The pipeline was developed using a Conda environment called:

```text
cellpose2
```

## Activate the environment

Open **Anaconda Prompt** or another terminal where Conda is available and run:

```bash
conda activate cellpose2
```

The environment should be activated before running the Python scripts.

## Check Python

Python can be checked using:

```bash
python --version
```

## Main Python packages

The pipeline uses several Python libraries, including:

* NumPy
* Pandas
* Matplotlib
* SciPy
* scikit-image
* tifffile
* Cellpose

Individual scripts may require additional packages.

---

# Project Structure

The project was originally developed using:

```text
D:\Conn_3dpipeline
```

The GitHub repository is organised as follows:

```text
KHynes_3Dpipeline/
│
├── README.md
│
├── notebooks/
│   ├── Image preparation scripts
│   ├── Synapse detection scripts
│   ├── Neuron processing scripts
│   ├── Matching scripts
│   ├── Visualisation scripts
│   └── Statistical analysis scripts
│
└── results/
    │
    ├── matching/
    ├── neuron_measurements/
    ├── statistics/
    └── visualizations/
```

The `notebooks` folder contains the Python scripts developed throughout the project. The folder name is retained from the original project structure even though the files are primarily `.py` scripts.

---

# 1. Image Conversion and Preparation

The first stage prepares the microscopy data for downstream analysis.

Individual fluorescence channels are converted into formats suitable for processing.

Relevant scripts include:

```text
convert_C00.py
convert_C01.py
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
```

The corresponding wild-type data are handled using the `WT` scripts.

---

# 2. Image Cropping

Large microscopy images are cropped to the regions required for analysis.

Relevant scripts include:

```text
crop_00.py
crop_01.py
crop_02.py
crop_WT_C01.py
```

Cropping reduces the amount of data that needs to be processed and ensures that analysis is performed on the intended region of the tissue.

---

# 3. Alignment and Volume Checks

The imaging channels need to correspond spatially before measurements can be made.

The following scripts are used to inspect alignment and image dimensions:

```text
check_alignment.py
check_volume.py
```

These checks help confirm that the different channels represent the same spatial region and that the image volumes have the expected dimensions.

---

# 4. Synapse Detection

Synaptic puncta are detected separately in the GlyT2 and Gephyrin channels.

GlyT2 is used to identify presynaptic glycinergic terminals, while Gephyrin is used to identify postsynaptic inhibitory synaptic structures.

Relevant scripts include:

```text
detect_synapse.py
detect_synapse_C01.py
detect_synapses.py
synquant_batch.py
synquant_batch.ijm
```

SynQuant is used as part of the synapse-detection workflow.

The detection stage produces the spatial coordinates of detected synaptic puncta.

These coordinates are then used during the synapse-to-neuron matching stage.

---

# 5. Neuron Segmentation

Individual neurons are identified using labelled segmentation masks.

Each neuron is represented by a unique integer label in the mask.

For example:

```text
0 = background
1 = neuron 1
2 = neuron 2
3 = neuron 3
...
```

The segmentation masks provide the spatial information needed to identify individual neurons and associate synaptic puncta with them.

Relevant scripts include:

```text
stack_masks.py
stack_masks_WT.py
neuron_measurement.py
visualize_neurons.py
```

---

# 6. Synapse-to-Neuron Matching

Synapse detection provides the location of each detected synaptic punctum, while neuron segmentation provides the location of each neuron.

The matching stage combines these two datasets.

The process:

1. Loads the neuron segmentation mask.
2. Identifies individual neuron labels.
3. Loads detected synapse coordinates.
4. Compares synapse locations with the neuron segmentation.
5. Assigns detected synapses to neurons.
6. Counts the assigned synapses for each neuron.
7. Saves the resulting measurements.

Relevant scripts include:

```text
match_synapse.py
match_synapse_C01.py
match_synapses.py
```

The matching process is performed for both GlyT2 and Gephyrin.

---

# 7. Per-Neuron Results

The matching stage produces a CSV dataset containing measurements for individual neurons.

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

These datasets are stored in:

```text
results/matching/
```

The main output files are:

```text
TDP43_synapse_counts.csv
TDP43_gephyrin_counts.csv
```

Because the same neuron set is used for both datasets, GlyT2 and Gephyrin measurements can be compared on a neuron-by-neuron basis.

---

# 8. Neuron Measurements

Measurements can also be calculated from the neuron segmentation masks.

These measurements provide quantitative information about the segmented neurons and can be used to investigate relationships between neuronal properties and synaptic input.

The main script is:

```text
neuron_measurement.py
```

Results are stored in:

```text
results/neuron_measurements/
```

---

# 9. Visualisation and Quality Control

Visualisation is used to check different stages of the pipeline and confirm that the detected structures are spatially aligned correctly.

The visualisation scripts can display:

* Individual imaging channels
* Detected synaptic puncta
* Neuron segmentation masks
* Neuron centroids
* Synapse-to-neuron matching
* Synapse counts associated with individual neurons
* 3D image volumes
* 3D neuron masks

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

Generated visualisations are stored in:

```text
results/visualizations/
```

Visual quality control is important because it allows image-processing and matching errors to be identified before relying on the quantitative results.

---

# 10. Statistical Analysis

The final per-neuron GlyT2 and Gephyrin datasets are used for statistical analysis.

The analysis includes:

* Descriptive statistics
* Synapse-count distributions
* Per-slice analysis
* GlyT2 vs Gephyrin comparison
* Paired statistical testing
* Correlation analysis

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

---

# Statistical Methods

## Descriptive Statistics

The following measurements are calculated for both synaptic markers:

* Total number of neurons
* Total synapses
* Mean synapses per neuron
* Median synapses per neuron
* Standard deviation
* Minimum synapse count
* Maximum synapse count

---

## Synapse Count Distributions

Histograms are generated to show the distribution of synapse counts across individual neurons.

This allows the variability in synaptic input between neurons to be examined.

---

## Per-Slice Analysis

Synapse counts are grouped by Z slice to examine how measurements vary through the depth of the analysed tissue.

---

## GlyT2 vs Gephyrin Comparison

GlyT2 and Gephyrin measurements are obtained from the same neurons.

A **Wilcoxon signed-rank test** is therefore used to compare the paired measurements.

---

## GlyT2-Gephyrin Correlation

The relationship between GlyT2 and Gephyrin counts is assessed using **Spearman's rank correlation coefficient**.

This determines whether neurons with higher GlyT2 counts also tend to have higher Gephyrin counts.

---

# Final Dataset

The final analysis contains:

**79,460 paired neurons**

The measured synapse counts are:

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

The paired comparison between GlyT2 and Gephyrin measurements produced:

```text
Wilcoxon statistic = 119,574,968
p = 3.15 × 10^-203
```

This indicates a statistically significant difference between the two paired measurements.

---

## Spearman Correlation

The relationship between GlyT2 and Gephyrin counts produced:

```text
Spearman rho = 0.7217
p < 0.001
```

This indicates a strong positive relationship between GlyT2 and Gephyrin synapse counts.

In general, neurons with higher GlyT2 counts also tended to have higher Gephyrin counts.

Because the analysis contains a large number of neurons, statistical significance should be considered alongside the size of the observed relationship and its biological relevance.

---

# Results

The `results` directory contains the outputs generated throughout the analysis.

## `results/matching/`

Contains the final per-neuron synapse matching datasets:

```text
TDP43_synapse_counts.csv
TDP43_gephyrin_counts.csv
```

---

## `results/neuron_measurements/`

Contains measurements calculated from the neuron segmentation masks.

---

## `results/statistics/`

Contains statistical summaries, tables, and analysis figures.

---

## `results/visualizations/`

Contains figures and other visual outputs used for quality control and interpretation.

---

# Running the Pipeline

## Step 1 — Activate the Conda environment

Open Anaconda Prompt or a terminal with Conda installed.

```bash
conda activate cellpose2
```

---

## Step 2 — Navigate to the project

If the project is stored in its original location:

```bash
cd D:\Conn_3dpipeline
```

If it has been moved to another location, replace the path with the location of the project.

---

## Step 3 — Run a Python script

Python scripts can be run using:

```bash
python script_name.py
```

For example:

```bash
python statistics.py
```

or:

```bash
python final_analysis.py
```

The scripts may contain file paths specific to the original analysis environment. These paths should be updated when running the pipeline on another computer.

---

# Main Scripts

| Script                    | Purpose                            |
| ------------------------- | ---------------------------------- |
| `convert_C00.py`          | Prepare the GlyT2 channel          |
| `convert_C01.py`          | Prepare the Gephyrin channel       |
| `crop_00.py`              | Crop C00 images                    |
| `crop_01.py`              | Crop C01 images                    |
| `crop_02.py`              | Crop neuron mask images            |
| `check_alignment.py`      | Check channel alignment            |
| `check_volume.py`         | Check image volume                 |
| `detect_synapse.py`       | Detect synaptic puncta             |
| `detect_synapse_C01.py`   | Detect Gephyrin puncta             |
| `synquant_batch.py`       | Run batch synapse detection        |
| `stack_masks.py`          | Process neuron masks               |
| `neuron_measurement.py`   | Measure segmented neurons          |
| `match_synapse.py`        | Match synapses to neurons          |
| `match_synapse_C01.py`    | Match Gephyrin synapses to neurons |
| `visualize_detections.py` | Visualise detected synapses        |
| `visualize_neurons.py`    | Visualise neuron masks             |
| `visualize_matching.py`   | Visualise synapse-neuron matching  |
| `statistics.py`           | Calculate statistical summaries    |
| `stats_2.py`              | Additional statistical analysis    |
| `all_stats.py`            | Combined statistical analysis      |
| `final_analysis.py`       | Perform final analysis             |

---

# Reproducibility

The pipeline is divided into separate stages so that individual parts of the analysis can be inspected, modified, or rerun independently.

The main workflow is:

```text
Image conversion
      ↓
Image cropping
      ↓
Alignment and volume checks
      ↓
Synapse detection
      ↓
Neuron segmentation
      ↓
Synapse-neuron matching
      ↓
Neuron measurements
      ↓
Visualisation
      ↓
Statistical analysis
```

This structure allows the workflow to be adapted for different datasets, experimental groups, or imaging channels.

---

# Future Development

The pipeline provides a foundation for further quantitative analysis of neuronal and synaptic organisation in 3D microscopy data.

Possible future extensions include:

* Normalising synapse counts by neuron size
* Adding additional neuronal morphology measurements
* Comparing different experimental groups
* Comparing wild-type and hTDP-43 datasets
* Analysing additional brain regions
* Adding additional synaptic markers
* Improving automated synapse-to-neuron assignment
* Automating synapse-detection parameter selection
* Performing more detailed 3D spatial analysis of synapses
* Extending the pipeline to other microscopy datasets

---

# Summary

This project developed a Python-based workflow for analysing 3D light-sheet microscopy data at the level of individual neurons.

The pipeline combines:

* Image processing
* Channel preparation
* Synapse detection
* Neuron segmentation
* Synapse-to-neuron matching
* Per-neuron measurements
* Visual quality control
* Statistical analysis

The final dataset contains **79,460 paired neurons** with GlyT2 and Gephyrin measurements.

The pipeline provides a way to move from large 3D microscopy datasets to quantitative measurements of synaptic input for individual neurons, creating a foundation for further investigation of synaptic organisation in the hTDP-43 mouse model.

---

# Author

**K. Hynes**

University of St Andrews
School of Neuroscience

## Repository

[KHynes 3D Synapse Analysis Pipeline](https://github.com/Allodi-Lab/KHynes_3Dpipeline)

