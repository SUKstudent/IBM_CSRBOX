# 🚀 Space Mission Intelligence — Mission Outcome Prediction

## 📌 Project Overview

Space Mission Intelligence is a Machine Learning project that predicts the outcome of space missions using historical space mission data.

The project includes data cleaning, preprocessing, feature engineering, Machine Learning model training, model evaluation, and visualization.

Two classification models are implemented:

- Logistic Regression
- Random Forest Classifier

---

## 🎯 Objectives

- Clean and preprocess the space mission dataset using Python
- Handle missing values and duplicate records
- Extract useful features from the mission date
- Preprocess numerical and categorical features
- Train Machine Learning classification models
- Compare model performance
- Evaluate predictions using accuracy, precision, recall, F1-score, and confusion matrix
- Save the trained Random Forest model for future use

---

## 📊 Dataset

The dataset used in this project is the **Space Missions Dataset** from Kaggle.

### Dataset Source

https://www.kaggle.com/datasets/keremkarayaz/space-missions

### Main Features

- `Company` — Company conducting the mission
- `Location` — Launch location
- `Date` — Mission date
- `Time` — Mission time
- `Rocket` — Rocket used
- `Mission` — Mission name/type
- `RocketStatus` — Rocket status
- `Price` — Mission cost
- `MissionStatus` — Mission outcome

---

## 🧹 Data Preprocessing

The following preprocessing steps were performed:

1. Loaded the dataset using Pandas
2. Checked dataset information and statistics
3. Identified missing values
4. Removed duplicate records
5. Filled missing `Time` values using the mode
6. Converted `Price` into numeric format
7. Filled missing `Price` values using the median
8. Converted `Date` into datetime format
9. Extracted `Year` and `Month` from the Date column
10. Removed the original `Date` column before model training
11. Applied StandardScaler to numerical features
12. Applied OneHotEncoder to categorical features

---

## 🤖 Machine Learning Models

### 1. Logistic Regression

Logistic Regression was used as a classification model and baseline for comparison.

### 2. Random Forest Classifier

- Random Forest was used as the second classification model.

- Parameters used:

- n_estimators = 200
- random_state = 42
- class_weight = balanced

- The class_weight='balanced' parameter was used because the mission outcome classes are imbalanced.

### 📈 Model Performance

The models were evaluated on a test dataset using an 80:20 train-test split.

- Model	Accuracy
- Logistic Regression	89.85%
- Random Forest	90.17%

-Accuracy is considered along with precision, recall, F1-score, and confusion matrix because the dataset contains imbalanced target classes.

### 🎯 Target Classes

- The target variable is:
   - MissionStatus

-The dataset contains the following mission outcome classes:

- Success
- Failure
- Partial Failure
- Prelaunch Failure
### 📊 Evaluation Metrics

The following metrics were used:

- Accuracy

- Precision

- Recall

- F1-score

- Confusion Matrix

- A confusion matrix was also generated for the Random Forest model to visualize the actual and predicted mission outcomes.

### 🛠️ Technologies Used

- Python

- Pandas

- NumPy

- Scikit-learn

- Matplotlib

- Joblib

### 📂 Project Structure

####Space-Mission-Intelligence/

│
├── README.md

├── train_model.py

├── requirements.txt

└── Project_Report.pdf

- The script performs data preprocessing, trains the models, evaluates their performance, and saves the Random Forest model.

## 💾 Saved Model

- After successful execution, the trained Random Forest model is saved as:
      -space_mission_model.pkl
