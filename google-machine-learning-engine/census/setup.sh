#!/bin/bash

run_script_local() {	
	cd estimator
	GCS_TRAIN_FILE=gs://cloud-samples-data/ml-engine/census/data/adult.data.csv
	GCS_EVAL_FILE=gs://cloud-samples-data/ml-engine/census/data/adult.test.csv

	CENSUS_DATA=data
	MODEL_DIR=output

	TRAIN_DATA=$CENSUS_DATA/adult.data.csv
	EVAL_DATA=$CENSUS_DATA/adult.test.csv

	if [ ! -f $TRAIN_DATA ] || [ ! -f $EVAL_DATA ]; then
		gsutil cp $GCS_TRAIN_FILE $TRAIN_DATA
		gsutil cp $GCS_EVAL_FILE $EVAL_DATA
	else
		rm -Rf $MODEL_DIR
	fi

	gcloud ml-engine local train \
		--module-name trainer.task \
		--package-path trainer/ \
		--job-dir $MODEL_DIR \
		-- \
		--train-files $TRAIN_DATA \
		--eval-files $EVAL_DATA \
		--train-steps 1000 \
		--eval-steps 100

	if [ $? = 0 ]; then
		echo "Python script succeeded!" && cd ..
		return 0
	fi
	
	echo "Python script failed!" && cd ..
	return 1
}

run_script_cloud() {
	cd estimator
	GCS_TRAIN_FILE=gs://cloud-samples-data/ml-engine/census/data/adult.data.csv
	GCS_EVAL_FILE=gs://cloud-samples-data/ml-engine/census/data/adult.test.csv
	
	BUCKET_NAME=census-118822
	CENSUS_DATA=data
	MODEL_DIR=output

	JOB_NAME=census_`date '+%Y%m%d_%H%M%S'`
	REGION=us-central1
	OUTPUT_PATH=gs://$BUCKET_NAME/$JOB_NAME

	CONFIG=../config.yaml

	gcloud ml-engine jobs submit training $JOB_NAME \
		--job-dir $OUTPUT_PATH \
		--runtime-version 1.4 \
		--config $CONFIG \
		--module-name trainer.task \
		--package-path trainer/ \
		--region $REGION \
		-- \
		--train-files $GCS_TRAIN_FILE \
		--eval-files $GCS_EVAL_FILE \
		--train-steps 1000 \
		--eval-steps 100

	if [ $? = 0 ]; then
		echo "Python script succeeded!" && cd ..
		return 0
	fi
	
	echo "Python script failed!" && cd ..
	return 1
}

if [ $1 ] && [ $1 == "cloud" ]; then
	run_script_cloud
else
	run_script_local
fi