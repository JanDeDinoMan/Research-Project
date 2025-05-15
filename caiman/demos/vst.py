
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import timeit
from tifffile import imwrite
from bm3d import bm3d, BM3DProfile

import caiman.external.houghvst.estimation as est
from caiman.external.houghvst.gat import compute_gat, compute_inverse_gat
import caiman as cm
from caiman.paths import caiman_datadir


def vst(inputfile, output):
    print('loaded:', inputfile)
    movie = cm.load(inputfile)
    movie = movie.astype(np.float32)

    # makes estimation numerically better:
    movie -= movie.mean()

    # use one every 200 frames
    temporal_stride = 100
    # use one every 8 patches (patches are 8x8 by default)
    spatial_stride = 6

    movie_train = movie[::temporal_stride]

    t = timeit.default_timer()
    estimation_res = est.estimate_vst_movie(movie_train, stride=spatial_stride)
    print('\tTime', timeit.default_timer() - t)

    alpha = estimation_res.alpha
    sigma_sq = estimation_res.sigma_sq
    sigma = np.sqrt(sigma_sq)

    movie_gat = compute_gat(movie, sigma_sq, alpha=alpha)
    # save movie_gat here
    movie_gat_inv = compute_inverse_gat(movie_gat, sigma_sq, alpha=alpha,
                                        method='asym')

    print(movie_gat_inv.dtype)
    movie_gat_inv = movie_gat_inv.astype(np.float32)
    imwrite(output.split('.')[0] + '_inv.tif', movie_gat_inv)
    print('inverse saved:', output.split('.')[0] + '_inv.tif')
    
    movie_denoised = np.zeros(movie_gat_inv.shape, dtype=np.float32)
    for i in range(240, 360):
        movie_denoised[i] = bm3d(movie_gat_inv[i], sigma_psd=sigma)

    imwrite(output, movie_denoised)
    print('Denoised:', output)


base = "/home/janwillem/Data/voltage_HPC2/"
vst(base + 'HPC2/00_02.tif', base + 'vst/00_02.tif')
vst(base + 'HPC2/00_03.tif', base + 'vst/00_03.tif')
vst(base + 'HPC2/00_02_mc.tif', base + 'vst/00_02_mc.tif')
vst(base + 'HPC2/00_03_mc.tif', base + 'vst/00_03_mc.tif')

base = "/home/janwillem/Data/Optosynth/"
vst(base + 'raw/optosynth__1__20__5.tif', base + 'vst/optosynth__1__20__5.tif')
vst(base + 'raw/optosynth__2__20__5.tif', base + 'vst/optosynth__2__20__5.tif')
vst(base + 'raw/optosynth__3__20__5.tif', base + 'vst/optosynth__3__20__5.tif')
vst(base + 'raw/optosynth__4__20__5.tif', base + 'vst/optosynth__4__20__5.tif')
vst(base + 'raw/optosynth__5__20__5.tif', base + 'vst/optosynth__5__20__5.tif')
