import os
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication

#Trocar os códigos abaixo pelos da sua instância!
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = os.getenv('RESOURCE_GROUP')
workspace_name = os.getenv('WORKSPACE_NAME')

svc_pr_password = os.environ.get("AZURE_CLIENT_SECRET")
svc_pr_id = os.environ.get("AZURE_CLIENT_ID")
tn_id = os.environ.get("AZURE_TENANT_ID")

svc_pr = ServicePrincipalAuthentication(
    tenant_id=tn_id,
    service_principal_id=svc_pr_id,
    service_principal_password=svc_pr_password)


ws = Workspace(
    subscription_id,
    resource_group,
    workspace_name,
    auth=svc_pr
    )

print("Found workspace {} at location {}".format(ws.name, ws.location))