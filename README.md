# hTDP-43: 3D Synapse Analysis Pipeline

## Overview

This repository contains a 3D image analysis pipeline developed to **analyze** synaptic inputs in light-sheet microscopy images from the hTDP-43 mouse model.

The main goal of the pipeline is to identify neurons, detect synaptic puncta, match synapses to individual neurons, and produce quantitative measurements that can be used to study synaptic connectivity.

The pipeline focuses on two synaptic markers:

- **GlyT2** — used as a marker of presynaptic glycinergic terminals.
- **Gephyrin** — used as a marker of postsynaptic sites.

The analysis was developed using Python, Cellpose, SynQuant, and several scientific image-processing libraries. The pipeline processes large microscopy datasets and produces both visual quality-control outputs and quantitative statistical results.

This repository contains the computational part of the project. The original microscopy datasets and large intermediate image files are not included because of their size.

---

# Project Structure

```text
KHynes_3Dpipeline/
│
├── notebooks/
│   ├── Overlay Elements of Synapse detection results.csv
│   ├── all_stats.py
│   ├── animate_slices.py
│   ├── batch_process.py
│   ├── batch_process_WT.py
│   ├── check_alignment.py
│   ├── check_volume.py
│   ├── convert_C00.py
│   ├── convert_C01.py
│   ├── convert_WT_C00.py
│   ├── convert_WT_C01.py
│   ├── convert_WT_C02.py
│   ├── crop_00.py
│   ├── crop_01.py
│   ├── crop_02.py
│   ├── crop_WT_C01.py
│   ├── detect_synapse.py
│   ├── detect_synapse_C01.py
│   ├── detect_synapses.py
│   ├── final_analysis.py
│   ├── make_3d_volume_gif.py
│   ├── make_slice_gif.py
│   ├── mask_3d_gif.py
│   ├── match_synapse.py
│   ├── match_synapse_C01.py
│   ├── match_synapses.py
│   ├── neuron_measurement.py
│   ├── stack_masks.py
│   ├── stack_masks_WT.py
│   ├── statistics.py
│   ├── stats_2.py
│   ├── synquant_batch.ijm
│   ├── synquant_batch.py
│   ├── visualization_matching.py
│   ├── visualize_all_channels.py
│   ├── visualize_detections.py
│   ├── visualize_detections_01.py
│   ├── visualize_matching.py
│   ├── visualize_matching2.py
│   ├── visualize_neurons.py
│   └── visualize_overlay.py
│
├── results/
│   │
│   ├── matching/
│   │   ├── TDP43_gephyrin_counts.csv
│   │   └── TDP43_synapse_counts.csv
│   │
│   ├── neuron_measurements/
│   │   ├── matching_quality.csv
│   │   └── per_neuron_measurements.csv
│   │
│   ├── statistics/
│   │   ├── FINAL_ANALYSIS_SUMMARY.csv
│   │   ├── Stats_Terminal.PNG
│   │   ├── glyt2_gephyrin_correlation.png
│   │   ├── glyt2_vs_gephyrin.png
│   │   ├── glyt2_vs_gephyrin_boxplot.png
│   │   ├── paired_neuron_comparison.png
│   │   ├── paired_neuron_data.csv
│   │   ├── paired_neuron_statistics.csv
│   │   ├── priority_statistical_tests.csv
│   │   ├── priority_summary_statistics.csv
│   │   ├── statistical_tests.csv
│   │   ├── summary_statistics.csv
│   │   ├── synapse_counts_by_Z_slice.png
│   │   ├── synapse_distributions.png
│   │   ├── synapse_per_slice.png
│   │   └── synapse_statistics_by_Z_slice.csv
│   │
│   └── visualizations/
│       ├── C01_detection_visualization.png
│       ├── alignment_check.png
│       ├── detection_visualization.png
│       ├── draft.txt
│       ├── full_overlay.png
│       ├── matching_visualization.png
│       ├── matching_visualization2.png
│       ├── matching_visualization_gephyrin.png
│       └── neuron_visualization.png
│
└── Progress_updates.txt
````

---

# Pipeline Overview

The analysis is divided into several main stages.

```text
Light-Sheet Microscopy Data
            │
            ▼
      Image Conversion
            │
            ▼
       Image Cropping
            │
            ▼
     Channel Processing
            │
            ▼
     Neuron Segmentation
            │
            ▼
     Synapse Detection
            │
            ▼
   Synapse-to-Neuron Matching
            │
            ▼
     Neuron Measurements
            │
            ▼
      Statistical Analysis
            │
            ▼
 Visualization + Quantitative Results
```

---

# 1. Image Conversion

The microscopy data are initially converted into TIFF format so that they can be processed using Python-based image analysis tools.

The conversion scripts include:

* `convert_C00.py`
* `convert_C01.py`

Additional scripts are included for the WT dataset:

* `convert_WT_C00.py`
* `convert_WT_C01.py`
* `convert_WT_C02.py`

The C00 and C01 channels correspond to the two synaptic markers used in the analysis.

For the TDP-43 dataset:

* **C00 = GlyT2**
* **C01 = Gephyrin**
* **C02 = neuron segmentation masks**

---

# 2. Image Cropping and Preparation

Large microscopy images are cropped into regions that can be processed more efficiently.

Scripts used for this stage include:

* `crop_00.py`
* `crop_01.py`
* `crop_02.py`

A WT-specific cropping script is also included:

* `crop_WT_C01.py`

Additional scripts such as `check_alignment.py` and `check_volume.py` can be used to check the image data before continuing with the analysis.

---

# 3. Neuron Segmentation

Neuron masks are generated to identify individual neurons within the microscopy images.

The segmentation masks are used to assign each neuron a unique identifier.

The pipeline then calculates the position of each neuron, including its centroid coordinates.

The main neuron measurement script is:

```text
neuron_measurement.py
```

The resulting measurements are stored in:

```text
results/neuron_measurements/
```

including:

```text
per_neuron_measurements.csv
matching_quality.csv
```

---

# 4. Synapse Detection

Synaptic puncta are detected separately for the different channels.

The main detection scripts include:

```text
detect_synapse.py
detect_synapse_C01.py
detect_synapses.py
```

SynQuant is also used as part of the synapse detection process.

The repository includes both:

```text
synquant_batch.py
synquant_batch.ijm
```

Detection visualizations can be generated using:

```text
visualize_detections.py
visualize_detections_01.py
```

These visualizations provide a way to check whether detected synaptic puncta are correctly positioned relative to the microscopy data.

---

# 5. Synapse-to-Neuron Matching

After neurons and synapses have been detected, synaptic puncta are assigned to individual neurons.

This allows the analysis to move from simply counting synapses across an image to calculating:

**number of synapses per neuron**

The matching scripts include:

```text
match_synapse.py
match_synapse_C01.py
match_synapses.py
```

The results are stored in:

```text
results/matching/
```

The main output files are:

```text
TDP43_synapse_counts.csv
TDP43_gephyrin_counts.csv
```

These contain information including:

* Z slice
* neuron ID
* neuron centroid X coordinate
* neuron centroid Y coordinate
* GlyT2 synapse count
* Gephyrin synapse count

This creates a neuron-level dataset that can be used for downstream statistical analysis.

---

# 6. Quality Control and Visualization

Several scripts were developed to visually inspect the different stages of the pipeline.

These include:

```text
visualize_all_channels.py
visualize_neurons.py
visualize_overlay.py
visualization_matching.py
visualize_matching.py
visualize_matching2.py
```

The resulting figures are stored in:

```text
results/visualizations/
```

Examples include:

* `alignment_check.png`
* `detection_visualization.png`
* `C01_detection_visualization.png`
* `neuron_visualization.png`
* `full_overlay.png`
* `matching_visualization.png`
* `matching_visualization2.png`
* `matching_visualization_gephyrin.png`

These figures are used to visually check image alignment, neuron segmentation, synapse detection, and synapse-to-neuron matching.

---

# 7. Statistical Analysis

Once the synapses have been matched to neurons, the resulting data can be statistically **analyzed**.

The main statistical scripts include:

```text
statistics.py
stats_2.py
all_stats.py
final_analysis.py
```

The statistical analysis includes measurements such as:

* Total number of neurons
* Total number of synapses
* Mean synapses per neuron
* Median synapses per neuron
* Standard deviation
* Minimum and maximum synapse counts
* GlyT2-to-Gephyrin ratios
* Per-Z-slice synapse counts
* Paired neuron comparisons
* Wilcoxon statistical testing
* Spearman correlation analysis

The statistical outputs are stored in:

```text
results/statistics/
```

This includes CSV files containing numerical results and PNG files containing plots.

---

# 8. Final Analysis

The final analysis combines the neuron-level data from the GlyT2 and Gephyrin datasets.

Because both datasets are derived from the same neuron set, the analysis can treat GlyT2 and Gephyrin measurements as paired observations.

The final analysis includes comparisons between presynaptic GlyT2 counts and postsynaptic Gephyrin counts.

The resulting outputs include:

```text
paired_neuron_data.csv
paired_neuron_statistics.csv
priority_statistical_tests.csv
priority_summary_statistics.csv
FINAL_ANALYSIS_SUMMARY.csv
```

Correlation and comparison figures include:

```text
glyt2_gephyrin_correlation.png
glyt2_vs_gephyrin.png
glyt2_vs_gephyrin_boxplot.png
paired_neuron_comparison.png
```

---

# 9. Per-Z-Slice Analysis

The dataset contains information about the Z slice in which each neuron was detected.

This allows synaptic measurements to be examined across tissue depth.

The pipeline produces:

```text
synapse_counts_by_Z_slice.png
synapse_per_slice.png
synapse_statistics_by_Z_slice.csv
```

These outputs can be used to identify changes in synapse counts across the depth of the light-sheet microscopy volume.

---

# Environment Setup

The pipeline was developed using a Conda environment called:

```text
cellpose2
```

## 1. Open Anaconda Prompt

Open **Anaconda Prompt** on Windows.

## 2. Activate the Environment

Run:

```bash
conda activate cellpose2
```

After activation, the command prompt should show something similar to:

```text
(cellpose2) C:\Users\YourName>
```

This indicates that the `cellpose2` environment is active.

## 3. Run Python Scripts

Navigate to the directory containing the repository or script and run a Python file using:

```bash
python script_name.py
```

For example:

```bash
python statistics.py
```

The exact paths used by some scripts may need to be changed depending on where the data are stored.

---

# Required Python Libraries

The scripts use a number of scientific Python libraries, including:

* NumPy
* pandas
* SciPy
* Matplotlib
* scikit-image
* tifffile
* Cellpose

PyTorch and other supporting packages may also be required by individual scripts.

The exact packages required depend on which part of the pipeline is being run.

---

# Data Not Included in This Repository

The raw microscopy data and large intermediate datasets are intentionally not included in GitHub.

This includes large collections of TIFF images and other files generated during processing, including:

```text
raw/
raw_converted/
cropped/
masks/
models/
training/
```

The raw dataset contains a large number of microscopy files, making it unsuitable for storage directly in this repository.

The repository therefore focuses on the **code, processed results, statistical outputs, and visualization outputs** required to document the analysis.

---

# TDP-43 and WT Pipeline

This repository primarily contains the completed analysis for the **hTDP-43 mouse model**.

The overall project is intended to include two sides:

1. **hTDP-43 mouse model**
2. **WT (wild-type) mouse model**

The hTDP-43 side of the pipeline was developed and **analyzed** during this project.

The WT component has not yet been completed and will be continued by another student during the next academic year.

Several WT-related scripts have already been included in the repository to provide a starting point for this future work, including:

```text
batch_process_WT.py
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
stack_masks_WT.py
crop_WT_C01.py
```

These scripts can be developed further when the WT microscopy data become available.

---

# Reproducibility

The repository is designed to keep the computational workflow together in one location.

The general workflow is:

```text
1. Convert microscopy data
2. Check image alignment and volume
3. Crop images
4. Generate neuron masks
5. Detect synapses
6. Match synapses to neurons
7. Calculate neuron-level measurements
8. Perform statistical analysis
9. Generate visualizations
10. Review final results
```

The raw microscopy data should be stored separately and supplied to the relevant processing stages.

Because some scripts contain paths specific to the original analysis environment, file paths may need to be modified before running the pipeline on another computer.

---

# Repository Outputs

The repository contains four main types of outputs.

### Matching

```text
results/matching/
```

Contains the neuron-level synapse matching datasets.

### Neuron Measurements

```text
results/neuron_measurements/
```

Contains measurements and quality-control information related to the neuron segmentation and matching process.

### Statistics

```text
results/statistics/
```

Contains numerical statistical results and figures generated from the matched neuron datasets.

### Visualizations

```text
results/visualizations/
```

Contains image-based quality-control and analysis figures.

---

# Progress Documentation

A project progress record is also included:

```text
Progress_updates.txt
```

This documents the development of the pipeline and can be used to understand how the analysis progressed throughout the project.

---

# Summary

This repository provides the computational framework for **analyzing** 3D light-sheet microscopy data from the hTDP-43 mouse model.

The pipeline combines:

* Image processing
* Neuron segmentation
* Synapse detection
* Synapse-to-neuron matching
* Neuron-level measurements
* Statistical analysis
* Visualization and quality control

The main output is a quantitative description of GlyT2 and Gephyrin synaptic measurements at the individual-neuron level.

The repository contains the code and analysis outputs while keeping the large microscopy datasets and intermediate files outside of GitHub.

The WT portion of the pipeline is intended to be completed and extended by a future student.
