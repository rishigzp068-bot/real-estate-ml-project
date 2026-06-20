# =========================================
# 1. IMPORT LIBRARIES
# =========================================
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

import warnings
warnings.filterwarnings("ignore")

# =========================================
# 2. LOAD DATA
# =========================================
clients = pd.read_excel("clients.xlsx")
properties = pd.read_excel("properties.xlsx")

print("Clients Shape:", clients.shape)
print("Properties Shape:", properties.shape)

# =========================================
# 3. DATA CLEANING
# =========================================
# Standardize column names
clients.columns = clients.columns.str.strip().str.replace(" ", "_")
properties.columns = properties.columns.str.strip().str.replace(" ", "_")

# Remove duplicates
clients = clients.drop_duplicates()
properties = properties.drop_duplicates()

# Fill missing values
for col in clients.select_dtypes(include=np.number):
    clients[col].fillna(clients[col].median(), inplace=True)

for col in clients.select_dtypes(include='object'):
    clients[col].fillna(clients[col].mode()[0], inplace=True)

for col in properties.select_dtypes(include=np.number):
    properties[col].fillna(properties[col].median(), inplace=True)

for col in properties.select_dtypes(include='object'):
    properties[col].fillna(properties[col].mode()[0], inplace=True)

print("Missing after cleaning:", clients.isnull().sum().sum())

# =========================================
# 4. MERGE DATA (if common column exists)
# =========================================
# Adjust column name if needed
common_cols = list(set(clients.columns) & set(properties.columns))

if len(common_cols) > 0:
    df = pd.merge(clients, properties, on=common_cols[0], how='inner')
else:
    df = clients.copy()

print("Final Dataset Shape:", df.shape)

# =========================================
# 5. FEATURE ENGINEERING
# =========================================
# Age Group
if 'Age' in df.columns:
    df['Age_Group'] = pd.cut(df['Age'],
                            bins=[0,25,40,60,100],
                            labels=['Young','Adult','Mid','Senior'])

# Buyer Type
if 'Income' in df.columns:
    df['Buyer_Type'] = pd.cut(df['Income'],
                             bins=[0,30000,70000,150000,1000000],
                             labels=['Low','Medium','High','Premium'])

# =========================================
# 6. ENCODING
# =========================================
le = LabelEncoder()

for col in df.select_dtypes(include='object'):
    df[col] = le.fit_transform(df[col])

# =========================================
# 7. SCALING
# =========================================
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# =========================================
# 8. K-MEANS CLUSTERING
# =========================================
kmeans = KMeans(n_clusters=4, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_data)

print("Clustering Done!")

# =========================================
# 9. PRICE PREDICTION MODEL
# =========================================
if 'Price' in df.columns and 'Income' in df.columns and 'Age' in df.columns:
    
    X = df[['Income', 'Age']]
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    print("Model MAE:", mae)

# =========================================
# 10. FINAL DATASET SAVE
# =========================================
file_name = "Final_Analyzed_RealEstate_Data.xlsx"
df.to_excel(file_name, index=False)

print("✅ Final Excel Saved!")

# =========================================
# 11. DOWNLOAD (COLAB)
# =========================================
from google.colab import files
files.download(file_name)
