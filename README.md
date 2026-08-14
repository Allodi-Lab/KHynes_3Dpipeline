# hTDP-43 - 3D Synapse Analysis Pipeline

## Overview

This repository contains the computational pipeline developed to analyse 3D light-sheet microscopy images from the hTDP-43 mouse model.

The project focuses on quantifying glycinergic synaptic inputs at the level of individual neurons. The pipeline processes large 3D microscopy datasets, identifies neurons and synaptic puncta, matches detected synapses to individual neurons, and produces quantitative measurements for further statistical analysis.

Two synaptic markers are analysed:

- **GlyT2** — a marker of presynaptic glycinergic terminals
- **Gephyrin** — a marker of postsynaptic inhibitory synaptic structures

Neuron segmentation masks are used to identify individual neurons and provide the spatial information required to associate detected synapses with specific neurons.

This repository represents the **hTDP-43 portion of a larger analysis pipeline**. The corresponding wild-type (WT) analysis will be completed separately by a subsequent student as part of the continuation of this project.

---

## Project Aim

The aim of the project was to develop a computational workflow for analysing 3D light-sheet microscopy data and quantifying synaptic input at the level of individual neurons.

The pipeline was designed to:

1. Prepare 3D microscopy images for analysis.
2. Separate and process the relevant imaging channels.
3. Detect GlyT2 and Gephyrin synaptic puncta.
4. Process neuron segmentation masks.
5. Identify individual neurons.
6. Match detected synapses to individual neurons.
7. Calculate synapse counts for each neuron.
8. Calculate additional neuronal measurements.
9. Visualise the results for quality control.
10. Perform statistical analysis of the resulting measurements.

---

# Project Structure

The complete local project directory is organised approximately as follows:

```text
Conn_3dpipeline/
│
├── cropped/
├── masks/
├── models/
├── notebooks/
├── raw/
├── raw_converted/
├── raw_converted_C00/
├── raw_converted_C00_converted/
├── raw_converted_C00_cropped/
├── raw_converted_C01/
├── raw_converted_C01_converted/
├── raw_converted_C01_cropped/
├── results/
├── training/
├── WT/
│
└── progress_updates.txt
````

Not all folders are included in the GitHub repository.

---

# GitHub Repository

The GitHub repository contains the analysis scripts and selected results:

```text
KHynes_3Dpipeline/
│
├── README.md
│
├── notebooks/
│
└── results/
    │
    ├── matching/
    ├── neuron_measurements/
    ├── statistics/
    └── visualizations/
```

The repository is intended to document and preserve the computational workflow rather than store the complete microscopy dataset.

---

# Data Not Included in GitHub

The full microscopy dataset and several intermediate files are stored separately from the GitHub repository.

The following directories are therefore **not included**:

```text
raw/
masks/
cropped/
models/
training/
raw_converted/
raw_converted_C00/
raw_converted_C00_converted/
raw_converted_C00_cropped/
raw_converted_C01/
raw_converted_C01_converted/
raw_converted_C01_cropped/
WT/
```

### Why are these files not included?

The raw and processed microscopy datasets contain a large number of TIFF files. In particular, the converted datasets contain approximately **921 TIFF files**, making them unsuitable for storage in a standard GitHub repository.

The raw microscopy data and intermediate processing files should therefore be maintained using the laboratory's appropriate data-storage system.

The `masks`, `models`, `training`, and other intermediate directories are also retained locally because they form part of the working analysis environment but are not required to store the core source code in this repository.

---

# hTDP-43 and WT Pipeline

The project is divided into two main parts:

```text
                 3D Synapse Analysis Pipeline
                            |
             ┌──────────────┴──────────────┐
             |                             |
          hTDP-43                         WT
             |                             |
       Current project               Future project
             |                             |
       This repository             Next student
```

## hTDP-43

The hTDP-43 portion of the pipeline was developed during this project.

It includes:

* Image preparation
* GlyT2 processing
* Gephyrin processing
* Synapse detection
* Neuron segmentation processing
* Synapse-to-neuron matching
* Neuron measurements
* Visualisation
* Statistical analysis

The final hTDP-43 analysis contains paired GlyT2 and Gephyrin measurements for individual neurons.

## Wild-Type (WT)

The WT portion of the analysis has not yet been completed.

The WT data and corresponding analysis will be developed by another student when they join the project for the next academic year.

The existing pipeline is intended to provide the starting point for this work. The WT analysis can follow the same general workflow used for the hTDP-43 data, allowing the two experimental groups to eventually be compared.

---

# Environment Setup

The pipeline was developed using a Conda environment called:

```text
cellpose2
```

Activate the environment using:

```bash
conda activate cellpose2
```

Python can then be run from the activated environment.

For example:

```bash
python statistics.py
```

---

# Pipeline Workflow

The hTDP-43 analysis follows the workflow:

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
```

---

# Imaging Channels

The analysis uses three main channels:

| Channel | Marker       | Purpose                                     |
| ------- | ------------ | ------------------------------------------- |
| C00     | GlyT2        | Presynaptic glycinergic terminals           |
| C01     | Gephyrin     | Postsynaptic inhibitory synaptic structures |
| C02     | Neuron masks | Identification of individual neurons        |

The GlyT2 and Gephyrin measurements are generated using the same set of neurons, allowing direct paired comparison.

---

# Synapse Detection

Synaptic puncta are detected separately in the GlyT2 and Gephyrin channels.

The detection stage produces the spatial coordinates of detected synaptic structures.

Relevant scripts include:

```text
detect_synapse.py
detect_synapse_C01.py
detect_synapses.py
synquant_batch.py
synquant_batch.ijm
```

---

# Neuron Segmentation

Individual neurons are represented using labelled segmentation masks.

Each neuron is assigned a unique integer identifier within the mask.

The segmentation masks provide the spatial information required for synapse-to-neuron matching.

Relevant scripts include:

```text
stack_masks.py
stack_masks_WT.py
neuron_measurement.py
visualize_neurons.py
```

---

# Synapse-to-Neuron Matching

Detected synaptic puncta are matched to individual neurons using their spatial locations and the neuron segmentation masks.

For each neuron, the pipeline records the number of associated GlyT2 and Gephyrin synaptic puncta.

The resulting datasets contain:

```text
Z_slice
neuron_id
neuron_x
neuron_y
GlyT2_synapse_count
```

for GlyT2, and:

```text
Z_slice
neuron_id
neuron_x
neuron_y
Gephyrin_synapse_count
```

for Gephyrin.

The final datasets are stored in:

```text
results/matching/
```

---

# Statistical Analysis

The per-neuron datasets are used to calculate descriptive statistics and perform comparisons between GlyT2 and Gephyrin measurements.

The analysis includes:

* Mean synapse count
* Median synapse count
* Standard deviation
* Minimum and maximum values
* Total synapse counts
* Per-slice analysis
* Paired GlyT2 vs Gephyrin comparison
* Spearman correlation analysis

The statistical results are stored in:

```text
results/statistics/
```

---

# Final hTDP-43 Dataset

The final analysis contains:

**79,460 paired neurons**

with:

* **993,397 total GlyT2 synapses**
* **1,161,821 total Gephyrin synapses**

Mean synapse counts were:

| Measurement                     | Result |
| ------------------------------- | -----: |
| Mean GlyT2 synapses/neuron      | 12.502 |
| Mean Gephyrin synapses/neuron   | 14.621 |
| Median GlyT2 synapses/neuron    |      0 |
| Median Gephyrin synapses/neuron |      0 |
| GlyT2 standard deviation        | 41.577 |
| Gephyrin standard deviation     | 41.035 |

A paired Wilcoxon signed-rank test produced:

```text
p = 3.15 × 10^-203
```

The Spearman correlation between GlyT2 and Gephyrin counts was:

```text
rho = 0.7217
p < 0.001
```

These results represent the current hTDP-43 analysis and provide a baseline for comparison with the WT dataset when that portion of the project is completed.

---

# Results Directory

The GitHub repository contains the generated analysis outputs:

```text
results/
│
├── matching/
│   └── Per-neuron synapse matching results
│
├── neuron_measurements/
│   └── Measurements from neuron segmentation
│
├── statistics/
│   └── Statistical analysis and summary results
│
└── visualizations/
    └── Quality-control and analysis figures
```

---

# Continuing the Project

The next stage of the project will be to apply and, where necessary, adapt the pipeline to the WT dataset.

The expected workflow is:

```text
WT microscopy data
        |
        v
Same preprocessing workflow
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
WT statistical analysis
        |
        v
hTDP-43 vs WT comparison
```

The existing scripts should provide a starting point for the next student, although file paths and dataset-specific parameters may need to be updated for the WT data.

The eventual goal is to allow quantitative comparison of neuronal and synaptic organisation between the hTDP-43 and WT conditions.

---

# Summary

This repository contains the computational component of a larger project investigating synaptic organisation in 3D light-sheet microscopy data.

The work represented here focuses on the **hTDP-43 mouse model** and provides a workflow for moving from large 3D microscopy images to quantitative measurements of synaptic input at the individual-neuron level.

The pipeline combines:

* Image processing
* Channel conversion
* Image cropping
* Synapse detection
* Neuron segmentation
* Synapse-to-neuron matching
* Neuron measurements
* Visual quality control
* Statistical analysis

The current hTDP-43 analysis contains measurements from **79,460 paired neurons**.

The corresponding WT analysis will be completed as the next stage of the project by a subsequent student. This repository therefore provides both the completed hTDP-43 analysis and the computational framework from which the WT analysis can be continued.

```
