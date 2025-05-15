#!/bin/bash
base="/home/janwillem/Data/voltage_HPC2"

cellmincer denoise \
               -d "$base/cellmincer/$1" \
               -o "$base/cellmincer/$1/" \
               --avi-frame-range 0 7000 \
               --model optosynth.ckpt
