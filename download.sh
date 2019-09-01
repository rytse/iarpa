#!/usr/bin/env bash

DOWNLOAD_PATH=$1
S3BUCKET=pins2-data-public

cd $(dirname $0)

echo "Starting download script. Downloading IARPA PINS testing data to $DOWNLOAD_PATH"

#   parallel -a abc-file echo

echo "aws s3 cp --recursive s3://$S3BUCKET/testing $DOWNLOAD_PATH"
aws s3 cp --recursive s3://$S3BUCKET/testing $DOWNLOAD_PATH

# for i in $(cat linear-test | xargs); do
#     file_name=$i
#     file_location=$DOWNLOAD_PATH/$file_name
#     echo "Downloading $file_name to $file_location"
#     aws s3 cp s3://$S3BUCKET/$file_name $file_location
# done;

echo "Done!"