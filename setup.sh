#!/usr/bin/env bash

# Set up conda env
conda create -n pins
conda activate pins
conda install -c conda-forge awscli

# Set up awscli
aws configure

# Set up local dir structure
mkdir data
mkdir data/linear
mkdir data/pulsed
mkdir data/meta

# Pull metadata
aws s3 ls s3://pins2-data-public --recursive > data/meta/ls.txt
aws s3api get-object --bucket pins2-data-public --key training/list.txt data/meta/train_list.txt
aws s3api get-object --bucket pins2-data-public --key testing/list.txt data/meta/test_list.txt
aws s3api get-object --bucket pins2-data-public --key training/sounding-params-linear.txt data/meta/linear_params.txt
aws s3api get-object --bucket pins2-data-public --key training/sounding-params-pulsed.txt data/meta/pulsed_params.txt

# Pull the first linear and the first pulsed training data files
aws s3api get-object --bucket pins2-data-public --key training/train-000.bin data/linear/train-000.bin
aws s3api get-object --bucket pins2-data-public --key training/train-000.png data/linear/train-000.png

aws s3api get-object --bucket pins2-data-public --key training/train-002.bin data/pulsed/train-002.bin
aws s3api get-object --bucket pins2-data-public --key training/train-002.png data/pulsed/train-002.png
