import numpy as np
import json
import ARC_gym.utils.tokenization as tok

# EVOLVE-BLOCK-START

def apply_solution(input_grids: np.array):
    # Input_grids is a list of input grids, each being a 2D numpy array that contains the pixels of each grid.
    return input_grids

# EVOLVE-BLOCK-END

def get_similarity(input_grids, output_grids):
    total_similarity = 0
    
    for idx in range(len(input_grids)):
        inp_grid = input_grids[idx]
        out_grid = output_grids[idx]

        # Get dimensions of both grids
        inp_rows, inp_cols = inp_grid.shape
        out_rows, out_cols = out_grid.shape
        
        # Find the overlapping region dimensions
        overlap_rows = min(inp_rows, out_rows)
        overlap_cols = min(inp_cols, out_cols)
        
        # Count matching cells in the overlapping region
        matching_cells = 0
        for i in range(overlap_rows):
            for j in range(overlap_cols):
                if inp_grid[i, j] == out_grid[i, j]:
                    matching_cells += 1
        
        # Calculate maximum number of cells between both grids
        max_cells = max(inp_rows * inp_cols, out_rows * out_cols)
        
        # Calculate similarity percentage for this pair
        similarity_percentage = (matching_cells / max_cells) if max_cells > 0 else 0
        total_similarity += similarity_percentage
    
    # Return average similarity across all grid pairs
    return total_similarity / len(input_grids) if len(input_grids) > 0 else 0

def split_XY(sequence):
    result = []
    current_sublist = []
    
    for num in sequence:
        current_sublist.append(num)
        if num == 2:
            result.append(current_sublist)
            current_sublist = []
    
    # Handle case where the sequence doesn't end with 2
    if current_sublist:
        result.append(current_sublist)
        
    x = result[0]
    y = result[1]
    
    x = tok.detokenize_grid_unpadded(x)
    y = tok.detokenize_grid_unpadded(y)

    return x, y

def load_data(ood_path):
    """
    Load data from JSON file and extract input_sequences.
    
    Args:
        ood_path (str): Path to the JSON file
        
    Returns:
        list: List of input_sequences from each object in the JSON file
    """
    with open(ood_path, 'r') as file:
        data = json.load(file)
    
    input_grids = []
    target_grids = []
    for obj in data:
        if 'input_sequence' in obj:
            tokenized_grids = obj['input_sequence']
            inp_grid, out_grid = split_XY(tokenized_grids)

            input_grids.append(inp_grid)
            target_grids.append(out_grid)

    # Convert tuples to lists for both input and target grids
    for idx, example in enumerate(input_grids):
        input_grids[idx] = np.array([list(grid) for grid in example])
        target_grids[idx] = np.array([list(grid) for grid in target_grids[idx]])

    return input_grids, target_grids

# This part remains fixed (not evolved)
# It ensures that OpenEvolve can consistently call the evolving function.
def run_search():
    OOD_path = 'ARC-AGI/ood_data1.json'

    # load the input grids from the json file
    input_grids, target_grids = load_data(OOD_path)

    pred_grids = apply_solution(input_grids)
    
    # calculate pixelwise similarity between output_grids and input_grids
    similarity_value = get_similarity(pred_grids, target_grids)

    return similarity_value

# Note: The actual structure of initial_program.py is determined by data_api.py.