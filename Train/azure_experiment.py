import os
from xml.etree.ElementTree import QName
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Experiment

#
import json
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")


def connectToAzureMLWorkspace():
    #Trocar os códigos abaixo pelos da sua instância!
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    resource_group = os.getenv('RESOURCE_GROUP')
    workspace_name = os.getenv('WORKSPACE_NAME')

    svc_pr_password = os.environ.get("AZURE_CLIENT_SECRET")
    svc_pr_id = os.environ.get("AZURE_CLIENT_ID")
    tnt_id = os.environ.get("AZURE_TENANT_ID")

    svc_pr = ServicePrincipalAuthentication(
        tenant_id=tnt_id,
        service_principal_id=svc_pr_id,
        service_principal_password=svc_pr_password)


    ws = Workspace(
        subscription_id,
        resource_group,
        workspace_name,
        auth=svc_pr
        )

    print("Found workspace {} at location {}".format(ws.name, ws.location))
    return ws

def startExperiment(ws, experiment_name):
    experiment = Experiment(workspace=ws, name=experiment_name)
    run = experiment.start_logging( display_name="My Run " + dt_string,
                            outputs="output",
                            snapshot_directory="output")
    return run
    
def logToExperiment(experiment, key, value):
    experiment.log(key, value)

def readMetadataJson(filename):
    f = open(filename)
    data = json.load(f)
    return data
    
#Main
metadata_json = readMetadataJson("output/metadata.json")
#
ws = connectToAzureMLWorkspace()
my_experiment = startExperiment(ws, "data_science_salary_predict")
#log json into experiment.
for key in metadata_json:   
    value = metadata_json[key]
    logToExperiment(my_experiment, key, value)

#Complete job.
my_experiment.complete()

    
#json load


