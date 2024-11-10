# -*- coding: utf-8 -*-
"""Copy of Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MFoGE_fWS2wDmXw4p4K32Xk1U2fn34UC
"""

pip install pyspark

import pandas as pd
import matplotlib.pyplot as plt

file_path = '/content/drive/MyDrive/bigdata analisis/datasets/hypertension_data.csv'

df = pd.read_csv(file_path)
df.head(10)

df.info()

df.isnull().sum()

df = df.dropna(subset=['sex'])

df.isnull().sum()

from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, DecisionTreeClassifier, NaiveBayes

# Inisialisasi SparkSession
spark = SparkSession.builder.appName("ModelExamples").getOrCreate()

# Dataframe dari kolom yang Anda sebutkan
data = [
    (63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1, 1),
    # Tambahkan baris data lainnya di sini
]

columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
]

df = spark.createDataFrame(data, columns)

# Menggabungkan fitur-fitur ke dalam satu vektor kolom
assembler = VectorAssembler(inputCols=[col for col in columns if col != 'target'], outputCol="features")
data = assembler.transform(df)

# Pemisahan dataset menjadi training dan testing set (80% train, 20% test)
train_data, test_data = data.randomSplit([0.8, 0.2], seed=123)

# Inisialisasi dan melatih model Decision Tree
dt = DecisionTreeClassifier(labelCol='target', featuresCol='features', maxBins=32)
dt_model = dt.fit(train_data)

# Inisialisasi dan melatih model Logistic Regression
lr = LogisticRegression(labelCol='target', featuresCol='features')
lr_model = lr.fit(train_data)

# Inisialisasi dan melatih model Random Forest
rf = RandomForestClassifier(labelCol='target', featuresCol='features')
rf_model = rf.fit(train_data)

# Inisialisasi dan melatih model Naive Bayes
nb = NaiveBayes(labelCol='target', featuresCol='features')
nb_model = nb.fit(train_data)

# Membuat prediksi pada testing data
dt_predictions = dt_model.transform(test_data)
lr_predictions = lr_model.transform(test_data)
rf_predictions = rf_model.transform(test_data)
nb_predictions = nb_model.transform(test_data)

# Menampilkan beberapa hasil prediksi (opsional)
dt_predictions.select("target", "prediction", "probability").show()
lr_predictions.select("target", "prediction", "probability").show()
rf_predictions.select("target", "prediction", "probability").show()
nb_predictions.select("target", "prediction", "probability").show()

# Evaluasi model (jika ada label sebenarnya pada test set)
from pyspark.ml.evaluation import BinaryClassificationEvaluator

evaluator = BinaryClassificationEvaluator(labelCol="target")
accuracy_dt = evaluator.evaluate(dt_predictions)
accuracy_lr = evaluator.evaluate(lr_predictions)
accuracy_rf = evaluator.evaluate(rf_predictions)
accuracy_nb = evaluator.evaluate(nb_predictions)

# Print akurasi model
print(f"Accuracy Decision Tree = {accuracy_dt}")
print(f"Accuracy Logistic Regression = {accuracy_lr}")
print(f"Accuracy Random Forest = {accuracy_rf}")
print(f"Accuracy Naive Bayes = {accuracy_nb}")

# Menutup SparkSession
spark.stop()
