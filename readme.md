# hTDP-43: 3D Synapse Analysis Pipeline
### Allodi Lab — University of St Andrews

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.5.1%20CUDA-orange)
![Cellpose](https://img.shields.io/badge/Cellpose-4.2.1-green)
![Institution](https://img.shields.io/badge/Allodi%20Lab-St%20Andrews-purple)
![Status](https://img.shields.io/badge/Status-TDP--43%20Complete-brightgreen)

---

## Overview

This repository contains a 3D image analysis pipeline developed to analyze synaptic inputs in light-sheet microscopy images from the hTDP-43 mouse model.

The main goal of the pipeline is to identify neurons, detect synaptic puncta, match synapses to individual neurons, and produce quantitative measurements that can be used to study synaptic connectivity.

The pipeline focuses on two synaptic markers:

- **GlyT2** — a marker of presynaptic glycinergic terminals
- **Gephyrin** — a marker of postsynaptic sites

The analysis was developed using Python, Cellpose, and several scientific image-processing libraries. The pipeline processes large microscopy datasets and produces both visual quality-control outputs and quantitative statistical results.

This repository contains the computational part of the project. The original microscopy datasets and large intermediate image files are not included because of their size.

---

## Project Structure

```text
KHynes_3Dpipeline/
│
├── notebooks/
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
│   ├── synquant_batch.ijm          ← legacy attempt (not used in final pipeline)
│   ├── synquant_batch.py           ← legacy attempt (not used in final pipeline)
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
│       ├── full_overlay.png
│       ├── matching_visualization.png
│       ├── matching_visualization2.png
│       ├── matching_visualization_gephyrin.png
│       └── neuron_visualization.png
│
└── Progress_updates.txt
```

---

## Pipeline Overview

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
     (Cellpose — custom model)
            │
            ▼
     Synapse Detection
     (blob_log — scikit-image)
            │
            ▼
   Synapse-to-Neuron Matching
   (KD-tree — scipy.spatial)
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

## Channel Assignment

For the TDP-43 dataset:

| Channel | Marker | Purpose |
|---------|--------|---------|
| C00 | GlyT2 (647 nm) | Presynaptic glycinergic terminals |
| C01 | Gephyrin (555 nm) | Postsynaptic scaffold protein |
| C02 | NF-H / NT | Motor neuron cell bodies — used for segmentation |

---

## 1. Image Conversion

The microscopy data are initially in OME-TIFF format and are converted to standard TIFF so that they can be processed using Python-based image analysis tools.

Conversion scripts:

```text
convert_C00.py    ← TDP-43 GlyT2 channel
convert_C01.py    ← TDP-43 Gephyrin channel
```

Additional scripts are included for the WT dataset:

```text
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
```

---

## 2. Image Cropping and Preparation

Large microscopy images are cropped to the ventral horn region of interest (x=6588, y=252, w=4992, h=7740) to focus the analysis on the area containing motor neurons and reduce processing time.

```text
crop_C00.py
crop_C01.py
crop_C02.py
crop_WT_C01.py
```

Additional scripts for checking image data before analysis:

```text
check_alignment.py    ← verifies coordinate alignment between channels
check_volume.py       ← checks 3D volume properties
```

---

## 3. Neuron Segmentation

Motor neurons are segmented from the C02 channel using a custom Cellpose model fine-tuned from `cpsam_v2` on approximately 82 manually annotated motor neurons.

**Cellpose model parameters:**

| Parameter | Value |
|-----------|-------|
| Base model | cpsam_v2 |
| Diameter | 28 µm |
| Cellprob threshold | -1.0 |
| Flow threshold | 0.4 |
| Channel | Grayscale |
| Training epochs | 100 |

Batch segmentation scripts:

```text
batch_process.py        ← TDP-43 C02 batch inference
batch_process_WT.py     ← WT C02 batch inference
stack_masks.py          ← stack 2D masks into 3D volume
stack_masks_WT.py       ← stack WT masks into 3D volume
```

Per-neuron measurements are calculated using:

```text
neuron_measurement.py
```

Results stored in:

```text
results/neuron_measurements/
    per_neuron_measurements.csv
    matching_quality.csv
```

---

## 4. Synapse Detection

Synaptic puncta are detected using `skimage.feature.blob_log` with auto-contrast preprocessing (2nd–98th percentile normalization). This approach was selected after testing SynQuantVid in FIJI — the legacy SynQuant scripts are retained in the repository for reference but are not part of the final pipeline.

**Detection parameters:**

| Parameter | Value |
|-----------|-------|
| min_sigma | 1 |
| max_sigma | 5 |
| threshold | 0.05 |
| Resolution | 50% downsampled for speed |
| Preprocessing | Auto contrast (2nd–98th percentile) |

Detection scripts:

```text
detect_synapses.py        ← GlyT2 presynaptic dots (C00)
detect_synapse_C01.py     ← Gephyrin postsynaptic dots (C01)
```

Detection visualizations:

```text
visualize_detections.py       ← GlyT2
visualize_detections_01.py    ← Gephyrin
```

---

## 5. Synapse-to-Neuron Matching

Detected synaptic puncta are assigned to individual neurons using a KD-tree nearest-neighbour search (`scipy.spatial.cKDTree`). Each dot is matched to the closest neuron centroid within a distance threshold of 300 pixels. Dot coordinates are offset-corrected from cropped image space to full image space (x+6588, y+252) before matching.

Matching scripts:

```text
match_synapses.py         ← GlyT2 to neurons
match_synapse_C01.py      ← Gephyrin to neurons
```

Results stored in:

```text
results/matching/
    TDP43_synapse_counts.csv     ← GlyT2 synapse count per neuron per slice
    TDP43_gephyrin_counts.csv    ← Gephyrin synapse count per neuron per slice
```

Each output file contains: Z slice, neuron ID, neuron centroid X, neuron centroid Y, synapse count.

---

## 6. Quality Control and Visualization

Visual inspection scripts:

```text
visualize_all_channels.py      ← all channels in one 6-panel figure
visualize_neurons.py           ← colored neuron segmentation overlay
visualize_overlay.py           ← channel overlay
visualize_matching.py          ← neurons coloured by synapse count
visualize_matching2.py
visualization_matching.py
```

Visualization outputs stored in:

```text
results/visualizations/
    alignment_check.png
    detection_visualization.png
    C01_detection_visualization.png
    neuron_visualization.png
    full_overlay.png
    matching_visualization.png
    matching_visualization2.png
    matching_visualization_gephyrin.png
```

---

## 7. Statistical Analysis

Statistical analysis scripts:

```text
statistics.py
stats_2.py
all_stats.py
final_analysis.py
```

Analysis includes:

- Total neurons and synapses
- Mean, median, standard deviation of synapses per neuron
- GlyT2 to Gephyrin ratios
- Per-Z-slice synapse counts
- Paired neuron comparisons (GlyT2 vs Gephyrin)
- Wilcoxon signed-rank testing
- Spearman correlation analysis

Statistical outputs:

```text
results/statistics/
    FINAL_ANALYSIS_SUMMARY.csv
    summary_statistics.csv
    statistical_tests.csv
    priority_statistical_tests.csv
    priority_summary_statistics.csv
    paired_neuron_data.csv
    paired_neuron_statistics.csv
    synapse_statistics_by_Z_slice.csv
    glyt2_vs_gephyrin_boxplot.png
    glyt2_gephyrin_correlation.png
    paired_neuron_comparison.png
    synapse_distributions.png
    synapse_per_slice.png
    synapse_counts_by_Z_slice.png
```

---

## 8. Per-Z-Slice Analysis

Synapse measurements are examined across tissue depth using the Z slice information recorded for each neuron.

```text
synapse_counts_by_Z_slice.png
synapse_per_slice.png
synapse_statistics_by_Z_slice.csv
```

---

## Environment Setup

The pipeline was developed using a conda environment called `cellpose2`.

### 1. Open Miniforge Prompt

### 2. Activate the environment

```bash
conda activate cellpose2
```

### 3. Run Python scripts

```bash
python script_name.py
```

Note: file paths in some scripts may need to be updated depending on where data are stored on your machine.

---

## Required Python Libraries

```bash
conda install pytorch torchvision pytorch-cuda=12.4 -c pytorch -c nvidia
pip install cellpose==4.2.1
pip install tifffile numpy pandas scipy matplotlib scikit-image imageio roifile jupyter pyimagej
```

---

## Data Not Included

The following folders are not included in this repository due to file size:

```text
raw/
raw_converted/
cropped/
masks/
models/
training/
```

The repository contains the code, processed results, statistical outputs, and visualization outputs only.

---

## TDP-43 and WT Pipeline Status

| Side | Status |
|------|--------|
| hTDP-43 mouse model | Complete |
| WT (wild-type) mouse model | In progress — to be continued |

The WT component is intended to be completed by a future student. The following scripts are already in place as a starting point:

```text
batch_process_WT.py
convert_WT_C00.py
convert_WT_C01.py
convert_WT_C02.py
stack_masks_WT.py
crop_WT_C01.py
```

---

## Reproducibility

General workflow:

```text
1. Convert microscopy data
2. Check image alignment and volume
3. Crop images to ventral horn ROI
4. Generate neuron masks (Cellpose)
5. Detect synaptic puncta (blob_log)
6. Match synapses to neurons (KD-tree)
7. Calculate neuron-level measurements
8. Perform statistical analysis
9. Generate visualizations
10. Review final results
```

---

## Progress Documentation

```text
Progress_updates.txt
```

Documents the development of the pipeline throughout the project.

---

## Citation

```
[To be added upon publication]
K. Hynes, Allodi Lab, University of St Andrews, 2026
```

**Cellpose:**
> Stringer, C., et al. (2021). Cellpose: a generalist algorithm for cellular segmentation. *Nature Methods*, 18(1), 100–106.

**scikit-image:**
> van der Walt, S., et al. (2014). scikit-image: image processing in Python. *PeerJ*, 2, e453.

**SynQuant** (referenced, not used in final pipeline):
> Wang, Y., et al. (2020). SynQuant: An automatic tool to quantify synapses from microscopy images. *Bioinformatics*, 36(5), 1599–1606.

---

## Acknowledgements

Developed by K. Hynes in the Allodi Lab, University of St Andrews, under the supervision of Dr Ilary Allodi.
Light-sheet microscopy data acquired at the LSM3D Facility, University of Edinburgh.
This work extends the 2D analysis pipeline described in Mora et al. (2024).

---

