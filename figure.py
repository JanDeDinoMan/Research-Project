import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tifffile import imread
# import opencv2


def plot(path: str, output: str, frame: int):
    tif = imread(path)
    frame = tif[frame]
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_visible(False)                   # turn off the patch

    plt.imsave(output, frame, format="png", cmap=plt.get_cmap('gray'))


def compare_plot(path: str, output: str, frame: int, x: int, y: int):
    tif = imread(path)

    if tif.shape == (15000, 116, 498):
        tif = tif[:, 2:114, 9:489]

    frame = tif[frame]

    print(frame.shape)
    # Define crop area
    width, height = 30, 30
    sub_fig = frame[y:y+height, x:x+width]

    # Compute aspect ratios
    full_ar = frame.shape[1] / frame.shape[0]  # width / height
    crop_ar = sub_fig.shape[1] / sub_fig.shape[0]

    # Create figure with proportional width ratios but same height
    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[full_ar, crop_ar], wspace=0.01)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # Display full image
    ax1.imshow(frame, cmap='gray')
    rect = patches.Rectangle((x,y), width, height, linewidth=1, edgecolor='r', facecolor='none')
    ax1.add_patch(rect)

    # Display crop
    ax2.imshow(sub_fig, cmap='gray')

    # Cleanup
    for ax in [ax1, ax2]:
        ax.set_aspect('equal')
        ax.axis('off')

    fig.patch.set_visible(False)
    plt.savefig(output, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)


def zoomed_plot(path: str, output: str, frame: int, x: int, y: int):
    tif = imread(path)

    if tif.shape == (15000, 116, 498):
        tif = tif[:, 2:114, 9:489]

    frame = tif[frame]
    width, height = 30, 30
    sub_fig = frame[y:y+height, x:x+width]
    crop_ar = sub_fig.shape[1] / sub_fig.shape[0]

    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(1, 1, width_ratios=[crop_ar], wspace=0.01)
    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(sub_fig, cmap='gray')
    ax1.axis('off')

    fig.patch.set_visible(False)
    plt.savefig(output, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)

def box_plot(path: str, output: str, frame: int, x: int, y: int):
    tif = imread(path)

    if tif.shape == (15000, 116, 498):
        tif = tif[:, 2:114, 9:489]

    frame = tif[frame]
    width, height = 30, 30
    full_ar = frame.shape[1] / frame.shape[0]  # width / height

    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(1, 1, width_ratios=[full_ar], wspace=0.01)
    ax1 = fig.add_subplot(gs[0])

    ax1.imshow(frame, cmap='gray')
    rect = patches.Rectangle((x,y), width, height, linewidth=1, edgecolor='r', facecolor='none')
    ax1.add_patch(rect)

    ax1.axis('off')

    fig.patch.set_visible(False)
    plt.savefig(output, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)

HPC2_base = '/home/janwillem/Data/voltage_HPC2/'
Optosynth_base = '/home/janwillem/Data/Optosynth/'

figure_dir = '/home/janwillem/Documents/CSE-2024-2025/RSP/Research-Project/figures/Optosynth/'
x,y = 170, 70
box_plot(Optosynth_base + 'raw/optosynth__3__20__5.tif', figure_dir + 'Optosynth_3.png', 300, x, y)
zoomed_plot(Optosynth_base + 'clean/optosynth__3__20__5.tif', figure_dir + 'optosynth_zoom_3.png', 300, x, y)
zoomed_plot(Optosynth_base + 'cellmincer/optosynth__3__20__5/denoised_tyx.tif', figure_dir + 'optosynth_cellmincer_3.png', 300, x, y)
zoomed_plot(Optosynth_base + 'pmd/optosynth__3__20__5.tif', figure_dir + 'optosynth_pmd_3.png', 300, x, y)
zoomed_plot(Optosynth_base + 'vst/optosynth__3__20__5.tif', figure_dir + 'optosynth_vst_3.png', 300, x, y)

figure_dir = '/home/janwillem/Documents/CSE-2024-2025/RSP/Research-Project/figures/HPC2/'
x,y = 202, 47
box_plot(HPC2_base + 'HPC2/00_02.tif', figure_dir + 'HPC2_00_02.png', 300, x, y)
zoomed_plot(HPC2_base + 'HPC2/00_02.tif', figure_dir + 'HPC2_zoom_3.png', 300, x, y)
zoomed_plot(HPC2_base + 'cellmincer/00_02_mc/denoised_tyx.tif', figure_dir + 'HPC2_cellmincer_2_mc.png', 300, x, y)
zoomed_plot(HPC2_base + 'pmd/00_02.tif', figure_dir + 'HPC2_pmd_3.png', 300, x, y)
zoomed_plot(HPC2_base + 'vst/00_02.tif', figure_dir + 'HPC2_vst_3.png', 300, x, y)
