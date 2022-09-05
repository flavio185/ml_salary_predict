from azure_experiment import AzureModel 

#Main
model_name = "data_science_salary_predict"
m1 = AzureModel()
m1.downloadModelArtifacts(model_name, target_dir="app", version=3)
