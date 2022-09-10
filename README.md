# ml_salary_predict

## Train
Folder: Train

Inside Train:

*train.py* should save artifacts in *output* directory.

output/model.joblib

output/encoder.joblib

train.py should save metrics in metadata.json.
output/metadata.json

requirements.py - project dependencies. Training script will download this dependencies before training.

ex.:

### For executing training and saving artifacts:
Go to Jenkins:
http://20.121.252.249:8080/job/azureStorage/19/console

Run ModelTrainAndSave Job passing this project git.

Check model at AzureML data-masters-workspace workspace.
Pipeline looks for Train/train.py for training and saving model in the Cloud.

