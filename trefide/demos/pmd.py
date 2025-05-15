import os
import numpy as np
import platform
print(platform.python_version())
import inspect
from tifffile import imread
from tifffile import imwrite

# Preprocessing Dependencies
from trefide.utils import psd_noise_estimate

# PMD Model Dependencies
from trefide.pmd import batch_decompose,\
                        batch_recompose,\
                        overlapping_batch_decompose,\
                        overlapping_batch_recompose,\
                        determine_thresholds
from trefide.reformat import overlapping_component_reformat


def pmd(filename, truncate, block_height, block_width, output):
    mov = np.ascontiguousarray(np.array(imread(filename), dtype='d'))
    #PMD requires yxt
    mov = np.ascontiguousarray(np.transpose(mov, (1, 2, 0)))
    if truncate:
        mov = np.ascontiguousarray(mov[2:114, 9:489, :])
    print('loaded:', filename, mov.shape)
    ###################################################################################
    #Config
    fov_height, fov_width, num_frames = mov.shape
    # Generous maximum of rank 50 blocks (safeguard to terminate early if this is hit)
    max_components = 50
    
    # Enable Decimation 
    max_iters_main = 10
    max_iters_init = 40
    d_sub = 2
    t_sub = 2
    
    # Defaults
    consec_failures = 3
    tol = 5e-3
    
    # Set Blocksize Parameters
    overlapping = True
    enable_temporal_denoiser = True
    enable_spatial_denoiser = True
    ####################################################################################

    spatial_thresh, temporal_thresh = determine_thresholds((fov_height, fov_width, num_frames),
                                                            (block_height, block_width),
                                                            consec_failures, max_iters_main, 
                                                            max_iters_init, tol, 
                                                            d_sub, t_sub, 5, True,
                                                            enable_temporal_denoiser,
                                                            enable_spatial_denoiser)
    print('Tresholds computed')

    if not overlapping:
        # Blockwise Parallel, Single Tiling
        spatial_components,\
        temporal_components,\
        block_ranks,\
        block_indices = batch_decompose(fov_height, fov_width, num_frames,
                                        mov, block_height, block_width,
                                        spatial_thresh, temporal_thresh,
                                        max_components, consec_failures,
                                        max_iters_main, max_iters_init, tol,
                                        d_sub, t_sub,
                                        enable_temporal_denoiser, enable_spatial_denoiser)
    
    else:    # Blockwise Parallel, 4x Overlapping Tiling
        arr = (fov_height, fov_width, num_frames,
                                                    mov, block_height, block_width,
                                                    spatial_thresh, temporal_thresh,
                                                    max_components, consec_failures,
                                                    max_iters_main, max_iters_init, tol,
                                                    d_sub, t_sub,
                                                    enable_temporal_denoiser, enable_spatial_denoiser)
        spatial_components,\
        temporal_components,\
        block_ranks,\
        block_indices,\
        block_weights = overlapping_batch_decompose(fov_height, fov_width, num_frames,
                                                mov, block_height, block_width,
                                                spatial_thresh, temporal_thresh,
                                                max_components, consec_failures,
                                                max_iters_main, max_iters_init, tol,
                                                d_sub, t_sub,
                                                enable_temporal_denoiser, enable_spatial_denoiser)
    print('Decompose finished')

    if not overlapping:  # Single Tiling (No need for reqweighting)
        mov_denoised = np.asarray(batch_recompose(spatial_components,
                                                temporal_components,
                                                block_ranks,
                                                block_indices))
    else:   # Overlapping Tilings With Reweighting
        mov_denoised = np.asarray(overlapping_batch_recompose(fov_height, fov_width, num_frames,
                                                            block_height, block_width,
                                                            spatial_components,
                                                            temporal_components,
                                                            block_ranks,
                                                            block_indices,
                                                            block_weights))
    print('Reconstruction finished')

    mov_compressed = mov_denoised.astype(np.float32)
    #shape needs to be tyx
    mov_compressed = mov_compressed.transpose(2, 0, 1)
    print('Writing to:', output)
    imwrite(output, mov_compressed)
    print('PMD DONE!')

block_height = 28
block_width = 40
base = "/root/trefide/Data/voltage_HPC2/"
pmd(base + 'HPC2/00_02.tif', True, block_height, block_width, base + 'pmd/00_02.tif')
pmd(base + 'HPC2/00_02_mc.tif', True, block_height, block_width, base + 'pmd/00_02_mc.tif')
pmd(base + 'HPC2/00_03.tif', True, block_height, block_width, base + 'pmd/00_03.tif')
pmd(base + 'HPC2/00_03_mc.tif', True, block_height, block_width, base + 'pmd/00_03_mc.tif')

block_height = 36
block_width = 32
base = "/root/trefide/Data/Optosynth/"
pmd(base + 'raw/optosynth__1__20__5.tif', False, block_height, block_width, base + 'pmd/optosynth__1__20__5.tif')
pmd(base + 'raw/optosynth__2__20__5.tif', False, block_height, block_width, base + 'pmd/optosynth__2__20__5.tif')
pmd(base + 'raw/optosynth__3__20__5.tif', False, block_height, block_width, base + 'pmd/optosynth__3__20__5.tif')
pmd(base + 'raw/optosynth__4__20__5.tif', False, block_height, block_width, base + 'pmd/optosynth__4__20__5.tif')
pmd(base + 'raw/optosynth__5__20__5.tif', False, block_height, block_width, base + 'pmd/optosynth__5__20__5.tif')
