# Importing important libraries

# For data cleaning 
import pandas as pd
import ssl
from joblib import dump

# For preprocessing and building model
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# For exporting model information.
import json
from sklearn.model_selection import cross_val_score
import sklearn
import sys
import os

#create output dir
path = os.path.join(os.getenv('PWD'), 'output')
os.makedirs(path,  exist_ok = True)


def importDataSet():
  ssl._create_default_https_context = ssl._create_unverified_context
  url = 'https://raw.githubusercontent.com/flavio185/ml-salary-predict/main/Train/ds_salaries.csv'
  dataset = pd.read_csv(url)
  return dataset

df = importDataSet()

# Drop unecessary columns
df.drop(["Unnamed: 0", "salary"], axis = 1, inplace = True)

df["work_year"] = df["work_year"].astype("str")

# Renaming columns entries for clarity

# Experience Level
#df["experience_level"] = df["experience_level"].map({"SE":"Senior", "MI":"Junior", "EN":"Entry", "EX":"Expert"})
# # Employment Type
#df["employment_type"] = df["employment_type"].map({"FT":"Full-time", "PT":"Part-time", "CT":"Contract", "FL":"Freelance"})
# # Remote Ratio
df["remote_ratio"] = df["remote_ratio"].map({0:"Onsite", 50:"Hybrid", 100:"Remote"})
# Company Size
#df["company_size"] = df["company_size"].map({"S":"Small", "M":"Medium", "L":"Large"})

###PRE PROCESSING

X = df.copy()
y = X.pop("salary_in_usd")

X.drop(["salary_currency", "company_location"], axis = 1, inplace = True)


##Split Categorical data into OneHotEncoder and LabelEncoder

X_nominal_data = X[["work_year", "job_title", "remote_ratio", "employee_residence"]].reset_index(drop=True)

X_ordinal_data = X[["experience_level", "employment_type", "company_size"]].reset_index(drop=True)
X_ordinal_data["experience_level"] = X_ordinal_data["experience_level"].map({"EN":1, "MI":2, "SE":3, "EX":4})
X_ordinal_data["employment_type"] = X_ordinal_data["employment_type"].map({"FL":1, "CT":2, "PT":3, "FT":4})
X_ordinal_data["company_size"] = X_ordinal_data["company_size"].map({"S":1, "M":2, "L":3})

enc = OneHotEncoder(drop="first")

enc.fit(X_nominal_data)

X_onehotencoded = enc.transform(X_nominal_data).toarray()
X_onehotencoded = pd.DataFrame(X_onehotencoded)



X = pd.concat([X_onehotencoded, X_ordinal_data], axis=1)

###Training
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size = 0.8, test_size = 0.2, random_state = 1)

# Using SVR that has the lowest MAE
svr = SVR()

model = SVR(C = 1, gamma = 1, kernel = "linear")
model.fit(X_train, y_train)
preds = model.predict(X_valid[:1])
print(preds)
dump(model, 'output/model.joblib') # save the model
dump(enc, 'output/encoder.joblib') # save the encoder

def validatingModel():
  scores = -1 * cross_val_score(model, X, y, scoring = "neg_mean_absolute_error", cv = 10)
  return scores.mean()

def generateMetrics():
  metadata = {
    "Tipo": "Regressor",
    "MAE": validatingModel(),
    "python": sys.version.replace('\n', ''),
    "Versao sklearn": sklearn.__version__,      
    "Model Name": type(model).__name__,
    "Model info": model.get_params()
  }
  return json.dumps( metadata )

metrics = generateMetrics()
# Writing to sample.json
with open("output/metadata.json", "w") as outfile:
    outfile.write(metrics)
