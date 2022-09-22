train.py should save artifacts in *output* directory.
output/model.joblib
output/encoder.joblib

train.py should save metrics in metadata.json.
output/metadata.json

ex.:

Go to Jenkins:
http://20.121.252.249:8080/job/ModelTrainAndSave/build?delay=0sec

Run ModelTrainAndSave Job passing this project git.

Check model at AzureML.
