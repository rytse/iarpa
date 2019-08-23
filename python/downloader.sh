for file in $(aws s3 ls s3://pins2-data-public/training/ | grep ".bin" | cut -d' ' -f4)
do
    echo $file
    echo "Downloading..."
    aws s3api get-object --bucket pins2-data-public --key training/$file $file
done
