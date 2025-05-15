#!/bin/bash

base="/home/janwillem/Data/voltage_HPC2"

cellmincer preprocess \
               -i "$base/HPC2/$1.tif" \
               -o "$base/cellmincer/$1" \
               --manifest ./manifest/HPC2.yaml \
               --config ./preprocess/HPC2.yaml
