from azure_experiment import AzureModel 

#Main
model_name = "data_science_salary_predict"
m1 = AzureModel()
m1.startExperimentRun(model_name)
m1.logMetadataJson()
m1.finishExperimentRun()
m1.registerModelArtifacts()
