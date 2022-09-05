import os
import json

from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Experiment
from azureml.core.model import Model
#
from datetime import datetime


class AzureModel:
    def __init__(self, model_name):
        self.model_name = model_name
        # datetime object containing current date and time
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d%m%Y%H%M%S")
        self.model_output_path = os.path.join(os.getenv('PWD'), 'output')
        #
        self.azml_workspace = self.connectToAzureMLWorkspace()
        
    def connectToAzureMLWorkspace(self):
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

    def startExperimentRun(self):
        #starta experimento no azureml
        #self.azml_workspace = azml_workspace
        #self.model_name = model_name
        self.experiment = Experiment(workspace=self.azml_workspace, name=self.model_name)
        #starta job no azure ml para treinamento ou log de modelos.
        self.run = self.experiment.start_logging( display_name="My Run " + self.dt_string,
                                outputs="output",
                                snapshot_directory="output")

    def finishExperimentRun(self):
        self.run.complete()

    def logToExperiment(self, key, value):
        #helper que faze log do chave: valor ao experimento.
        self.key = key
        self.value = value
        self.run.log(key, value)

    def logMetadataJson(self):
        #Faz o registro do json de metadados de um modelo ao experimento.
        self.filename = "output/metadata.json"
        f = open(self.filename)
        data = json.load(f)
        for key in data:   
            value = data[key]
            self.logToExperiment(key, value)
        
    def registerModelArtifacts(self):
        Model.register(workspace=self.azml_workspace,
                    model_path=self.model_output_path,
                    model_name=self.model_name
                    )

    def downloadModelArtifacts(ws, model_name):
        model = Model(ws, name=model_name)
        model.download()


#Main
model_name = "data_science_salary_predict"
m1 = AzureModel(model_name)
m1.startExperimentRun()
m1.logMetadataJson()
m1.finishExperimentRun()
m1.registerModelArtifacts()
