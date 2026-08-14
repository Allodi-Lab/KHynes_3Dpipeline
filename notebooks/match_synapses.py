import pandas as pd
import numpy as np
import tifffile
import os
from scipy.spatial import cKDTree


masks_folder = r"D:\Conn_3dpipeline\masks"
synquant_folder = r"D:\Conn_3dpipeline\results\C00_synquant"  # C00 = GlyT2
output_folder = r"D:\Conn_3dpipeline\results\matching"

os.makedirs(output_folder, exist_ok=True)

mask_files = sorted([f for f in os.listdir(masks_folder) 
                     if f.endswith('_cp_masks.tif')])

print(f"Found {len(mask_files)} mask files")

all_results = []

for mask_filename in mask_files:
    z_num = mask_filename.split('_Z')[-1].replace('_cp_masks.tif', '')
    
    csv_filename = mask_filename.replace('_cp_masks.tif', '_synquant.csv')
    csv_path = os.path.join(synquant_folder, csv_filename)
    
    if not os.path.exists(csv_path):
        print(f"No SynQuant results for Z{z_num} — skipping")
        continue
    
    # ============================================================
    #Loading neuron center points from Cellpose mask
    # ============================================================
    mask = tifffile.imread(os.path.join(masks_folder, mask_filename))
    
    neuron_ids = np.unique(mask)
    neuron_ids = neuron_ids[neuron_ids > 0]
    
    neuron_centroids = []
    for nid in neuron_ids:
        positions = np.where(mask == nid)
        cy = np.mean(positions[0])
        cx = np.mean(positions[1])
        neuron_centroids.append((nid, cx, cy))
    
    if len(neuron_centroids) == 0:
        continue
        
    neuron_array = np.array([(cx, cy) for _, cx, cy in neuron_centroids])
    
    # ============================================================
    #Load GlyT2 synaptic dot positions from SynQuant CSV
    #(C00 = GlyT2 presynaptic channel)
    # ============================================================
    df = pd.read_csv(csv_path)
    
    if len(df) == 0:
        continue
    
    dot_positions = df[['X', 'Y']].values
    
    # ============================================================
    #Matching the dots to nearest neuron
    # ============================================================
    tree = cKDTree(neuron_array)
    threshold = 300
    
    distances, indices = tree.query(dot_positions, distance_upper_bound=threshold)
    
    synapse_counts = {nid: 0 for nid, _, _ in neuron_centroids}
    
    for dot_idx, (dist, neuron_idx) in enumerate(zip(distances, indices)):
        if dist < threshold and neuron_idx < len(neuron_centroids):
            nid = neuron_centroids[neuron_idx][0]
            synapse_counts[nid] += 1
    
    # ============================================================
    #Saving the results for this slice
    # ============================================================
    for nid, cx, cy in neuron_centroids:
        all_results.append({
            'Z_slice': z_num,
            'neuron_id': nid,
            'neuron_x': cx,
            'neuron_y': cy,
            'GlyT2_synapse_count': synapse_counts[nid]
        })
    
    print(f"Z{z_num}: {len(neuron_centroids)} Neurons, {sum(synapse_counts.values())} Synapses Matched")


#Saving the final results
# ============================================================
results_df = pd.DataFrame(all_results)
output_path = os.path.join(output_folder, 'TDP43_synapse_counts.csv')
results_df.to_csv(output_path, index=False)

print(f"\nDone")
print(f"Total neurons: {len(results_df)}")
print(f"Mean GlyT2 Synapses Per Neuron: {results_df['GlyT2_synapse_count'].mean():.2f}")
print(f"Total Synapses Matched: {results_df['GlyT2_synapse_count'].sum()}")