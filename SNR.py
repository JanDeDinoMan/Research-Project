import numpy as np
from tifffile import imread
import csv
import random
import json

rng = np.random.default_rng()

def read_tif_normalized(path: str) -> np.ndarray:
    tif = imread(path)
    print(tif.dtype)
    tif = tif.astype(np.float32)

    if tif.shape == (15000, 116, 498):
        tif = tif[:, 2:114, 9:489]
    print('processed:', tif.shape, tif.dtype)
    return tif


def get_SNR(ground_truth: np.ndarray, denoised: np.ndarray) -> float:
    signal_power = np.sum(ground_truth ** 2)
    noise_power = np.sum((ground_truth - denoised) ** 2)
    snr = signal_power / noise_power
    snr_db = 10 * np.log10(snr)
    return snr_db

def get_PSNR(clean: np.ndarray, denoised: np.ndarray, max_pixel=1.0) -> float:
    """Compute PSNR in decibels."""
    mse = np.mean((clean - denoised) ** 2)
    return 10 * np.log10((max_pixel ** 2) / mse)


def get_mean_PSNR(clean: np.ndarray, denoised: np.ndarray, max_pixel=1.0) -> float:
    psnr_list = []
    I_max = clean.max()
    for i in range(clean.shape[0]):
        mse = np.mean((clean[i] - denoised[i]) ** 2)
        if mse == 0:
            psnr = float('inf')
        else:
            psnr = ((I_max ** 2) / mse)
        psnr_list.append(psnr)
    return 10 * np.log10(np.mean(psnr_list))




def tsnr_2d(denoised: np.ndarray):
    mu = np.mean(denoised, axis=0)                    # mean over time for each pixel
    N = denoised.shape[0]                             
    sigma = np.sqrt(np.sum((denoised - mu) ** 2, axis=0) / N)  # population std

    tsnr_vals = np.where(sigma == 0, float('inf'), mu / sigma)
    return np.mean(tsnr_vals)



def run_optosynth():
    with open('data_optosynth.csv', newline='') as csvfile:
        csvData = csv.reader(csvfile, delimiter=',')
        
        # Skip header
        next(csvData)

        res= dict({
            'pmd': [],
            'cellmincer': [],
            'vst': [],
            'raw': [],
        })

        for row in csvData:
            ground_truth = read_tif_normalized(row[2])
            denoised = read_tif_normalized(row[3])
            method = row[1]

            if method == 'vst':
                denoised = denoised[245:340]
                ground_truth = ground_truth[245:340]
                denoised = np.where(denoised < 0, 0)

            print(row[3], 'Equal shape: ', ground_truth.shape == denoised.shape, '| Equal type: ', ground_truth.dtype == denoised.dtype)

            snr = get_SNR(ground_truth, denoised)
            psnr = get_mean_PSNR(ground_truth, denoised)
            tsnr = tsnr_2d(denoised)
            row = [snr, psnr, tsnr]
            res[method].append(row)
            print(row)

        print(res)


        
        pmd_results = list(np.round(np.mean(res['pmd'], axis=0),2))
        cellmincer_results = list(np.round(np.mean(res['cellmincer'], axis=0), 2))
        vst_results = list(np.round(np.mean(res['vst'], axis=0), 2))
        raw_results = list(np.round(np.mean(res['raw'], axis=0), 2))

        results = []
        results.append(['Method','SNR', 'PSNR', 'TSNR'])
        results.append(['PMD'] + pmd_results)
        results.append(['CellMincer'] + cellmincer_results)
        results.append(['VST'] + vst_results)
        results.append(['Raw'] + raw_results)


        with open('res_optosynth.csv', 'w') as csvfile:
            resCSV = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in results:
                resCSV.writerow(line)
run_optosynth()



def run_hpc2():
    with open('data_hpc2.csv', newline='') as csvfile:
        csvData = csv.reader(csvfile, delimiter=',')
        
        # Skip header
        next(csvData)

        res= dict({
            'pmd': [],
            'cellmincer': [],
            'vst': [],
            'raw': [],
            'cellmincer_mc': [],
            'pmd_mc': [],
            'raw_mc': [],
        })

        for row in csvData:
            denoised = read_tif_normalized(row[2])
            method = row[1]

            if method == 'vst':
                denoised = denoised[245:340]
            if method == 'vst':
                denoised = np.where(denoised < 0, 0)

            tsnr = tsnr_2d(denoised)
            res[method].append(tsnr)
            print(row)

        print(res)


        
        pmd_results = [np.round(np.mean(res['pmd']),2)]
        cellmincer_results = [np.round(np.mean(res['cellmincer']), 2)]
        vst_results = [np.round(np.mean(res['vst']), 2)]
        raw_results = [np.round(np.mean(res['raw']), 2)]

        pmd_mc_results = [np.round(np.mean(res['pmd_mc']),2)]
        cellmincer_mc_results = [np.round(np.mean(res['cellmincer_mc']), 2)]
        raw_mc_results = [np.round(np.mean(res['raw_mc']), 2)]


        results = []
        results.append(['Method','SNR', 'PSNR', 'TSNR'])
        results.append(['PMD'] + pmd_results)
        results.append(['CellMincer'] + cellmincer_results)
        results.append(['VST'] + vst_results)
        results.append(['Raw'] + raw_results)
        results.append(['PMD MC'] + pmd_mc_results)
        results.append(['CellMincer MC'] + cellmincer_mc_results)
        results.append(['Raw MC'] + raw_mc_results)



        with open('res_hpc2.csv', 'w') as csvfile:
            resCSV = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for line in results:
                resCSV.writerow(line)

run_hpc2()
