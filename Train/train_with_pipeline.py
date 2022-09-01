# Importing important libraries

# For data cleaning 
import pandas as pd
import numpy as np
import ssl
from joblib import dump

# For preprocessing and building model
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
#
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error


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
#X_ordinal_data["experience_level"] = X_ordinal_data["experience_level"].map({"EN":1, "MI":2, "SE":3, "EX":4})
#X_ordinal_data["employment_type"] = X_ordinal_data["employment_type"].map({"FL":1, "CT":2, "PT":3, "FT":4})
#X_ordinal_data["company_size"] = X_ordinal_data["company_size"].map({"S":1, "M":2, "L":3})

#le = LabelEncoder()
#le.fit(["EN", "MI", "SE", "EX", "FL", "CT", "PT", "FT", "S", "M", "L"])
#le.transform(X_ordinal_data["experience_level"], )

# pipeline para pré-processamento variaveis categoricas ordinais.
nominal_transformer = Pipeline(steps=[
    ('one-hot encoder', OneHotEncoder(drop="first"))
])

# pipeline para pré-processamento variaveis categoricas numerais.
ordinal_transformer = Pipeline(steps=[
    ('label encoder', OrdinalEncoder(categories='auto'))
])


#columnTransformer = ColumnTransformer([('encoder', OrdinalEncoder(), ["company_size"])])
#columnTransformer.fit_transform(X_train)
#df_transformed = pd.DataFrame(columnTransformer.fit_transform(X_ordinal_data), columns=["company_size"])

#print(df_transformed)
#print(X_ordinal_data["company_size"])
# Compondo os pré-processadores
preprocessor = ColumnTransformer(transformers=[
    ('one_hot_encoder', nominal_transformer, ["work_year", "job_title", "remote_ratio", "employee_residence"]),
    ('exp_lab_enc', ordinal_transformer, ["experience_level"]),
    ('emp_lab_enc', ordinal_transformer, ["employment_type"]), 
    ('comp_lab_enc', ordinal_transformer, ["company_size"])
])

#preprocessor.fit_transform(X)
#print(preprocessor)
# criando o modelo usando pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('svr', SVR(C = 1, gamma = 1, kernel = "poly"))
])

from sklearn.pipeline import make_pipeline
pipeline = make_pipeline(
    ('preprocessor', preprocessor),
    ('svr', SVR(C = 1, gamma = 1, kernel = "poly"))
)

X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size = 0.8, test_size = 0.2, random_state = 1)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
accuracy_score(y_test, y_pred)

#############################
###Somente transformando dados.
#a = model.fit_transform(X).toarray()
#df = pd.DataFrame(a)
#print(df.describe())

#print(df.head())

####################


X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size = 0.8, test_size = 0.2, random_state = 1)


###Training

#model.fit(X_train, y_train)

#print(X_train, y_train)
# Using SVR that has the lowest MAE
#svr = SVR()

#model = SVR(C = 1, gamma = 1, kernel = "poly")
model.fit(X, y)

#############

#scores = -1 * cross_val_score(model, X, y, scoring = "neg_mean_absolute_error", cv = 10)
#print("MEA",scores.mean())
preds = model.predict(X_valid)
MAE = mean_absolute_error(preds, y_valid)
print(MAE)
#preds = model.predict(X_valid)
#print(preds)
#print(y_valid[:-1])
#print(y_valid[:1])

#dump(model, 'model.joblib') # save the model
#dump(enc, 'encoder.joblib') # save the encoder