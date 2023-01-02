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

## API

API should have dockerize the model and make ready for deployment.

API will download output folder from azure ML. Version of model can be passed as parameter. If no parameter, last model saved will be downloaded.
Output folder will be available at: /code/app/output/

curl --location --request POST 'http://34.72.27.5/api' \
--header 'Content-Type: application/json' \
--data-raw '{
    "experience_level": "Senior",
    "employment_type": "Full-time",
    "company_size": "Small",
    "work_year": "2020",
    "job_title": "Data Scientist",
    "remote_ratio": "Remote",
    "employee_residence": "DE"
}'
