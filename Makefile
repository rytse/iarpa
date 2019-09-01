S3BUCKET=pins2-data-public

.PHONY: setup-aws
setup-aws:
	aws configure

.PHONY: setup-conda
setup-conda:
	conda create -n pins
	conda activate pins
	conda install -c conda-forge awscli

data:
	mkdir data
	mkdir data/linear
	mkdir data/pulsed
	mkdir data/meta

.PHONY: metadata
metadata:
	# Pull metadata
	aws s3 ls s3://pins2-data-public --recursive > data/meta/ls.txt
	aws s3 cp s3://$(S3BUCKET)/training/list.txt data/meta/train_list.txt
	aws s3 cp s3://$(S3BUCKET)/testing/list.txt data/meta/test_list.txt
	aws s3 cp s3://$(S3BUCKET)/training/sounding-params-linear.txt data/meta/linear_params.txt
	aws s3 cp s3://$(S3BUCKET)/training/sounding-params-pulsed.txt data/meta/pulsed_params.txt

.PHONY: iqdata
iqdata:
	# Pull the first linear and the first pulsed training data files
	aws s3 cp s3://$(S3BUCKET)/training/train-000.png data/linear/train-000.png
	aws s3 cp s3://$(S3BUCKET)/training/train-000.png data/linear/train-000.png

	aws s3 cp s3://$(S3BUCKET)/training/train-002.bin data/pulsed/train-002.bin
	aws s3 cp s3://$(S3BUCKET)/training/train-002.png data/pulsed/train-002.png

.PHONY: all
all: data metadata iqdata