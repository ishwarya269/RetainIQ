import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# ============================================================
# RETAINIQ - CUSTOMER CHURN PREDICTION
# ============================================================

print("\n============================================================")
print("RETAINIQ - CUSTOMER CHURN PREDICTION")
print("============================================================")


# ============================================================
# 1. LOAD DATA
# ============================================================

file_path = "data/processed/telco_churn_cleaned.csv"

print("\n===== LOADING DATASET =====")

df = pd.read_csv(file_path)

print("Dataset loaded successfully.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", "_", regex=True)
)


# ============================================================
# 3. CLEAN NUMERIC COLUMNS
# ============================================================

numeric_columns = [
    "Tenure_Months",
    "Monthly_Charges",
    "Total_Charges",
    "CLTV"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# 4. CREATE TARGET
# ============================================================

print("\n===== PREPARING TARGET =====")

df["Churn_Target"] = pd.to_numeric(
    df["Churn_Value"],
    errors="coerce"
)

df = df.dropna(
    subset=["Churn_Target"]
)

df["Churn_Target"] = df["Churn_Target"].astype(int)

print("Target created successfully.")

print("\nTarget distribution:")
print(df["Churn_Target"].value_counts())


# ============================================================
# 5. REMOVE DATA LEAKAGE
# ============================================================

# These columns reveal the outcome or are generated after churn.
# They must NOT be used as model predictors.

columns_to_remove = [
    "CustomerID",
    "Count",
    "Count_Value",
    "Churn_Label",
    "Churn_Value",
    "Churn_Score",
    "Churn_Reason",
    "Churn_Target"
]

existing_columns_to_remove = [
    column
    for column in columns_to_remove
    if column in df.columns
]

X = df.drop(
    columns=existing_columns_to_remove
)

y = df["Churn_Target"]


# ============================================================
# 6. IDENTIFY COLUMN TYPES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object"]
).columns.tolist()

numeric_columns = X.select_dtypes(
    include=[np.number]
).columns.tolist()

print("\n===== FEATURES =====")

print("Numeric features:", len(numeric_columns))
print("Categorical features:", len(categorical_columns))


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

print("\n===== SPLITTING DATA =====")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# 8. NUMERIC PIPELINE
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        )
    ]
)


# ============================================================
# 9. CATEGORICAL PIPELINE
# ============================================================

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


# ============================================================
# 10. PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_columns
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_columns
        )
    ]
)


# ============================================================
# 11. MODEL
# ============================================================

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)


# ============================================================
# 12. COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# 13. TRAIN MODEL
# ============================================================

print("\n===== TRAINING MODEL =====")

pipeline.fit(
    X_train,
    y_train
)

print("Model training completed successfully.")


# ============================================================
# 14. MAKE PREDICTIONS
# ============================================================

print("\n===== MAKING PREDICTIONS =====")

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(
    X_test
)[:, 1]

print("Predictions completed.")


# ============================================================
# 15. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n============================================================")
print("MODEL PERFORMANCE")
print("============================================================")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")


# ============================================================
# 16. CLASSIFICATION REPORT
# ============================================================

print("\n===== CLASSIFICATION REPORT =====")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 17. CONFUSION MATRIX
# ============================================================

print("\n===== CONFUSION MATRIX =====")

matrix = confusion_matrix(
    y_test,
    y_pred
)

print(matrix)


# ============================================================
# 18. CREATE TEST RESULTS
# ============================================================

results = X_test.copy()

results["Actual_Churn"] = y_test.values

results["Predicted_Churn"] = y_pred

results["Churn_Probability"] = (
    y_probability * 100
).round(2)


# ============================================================
# 19. CREATE RISK LEVEL
# ============================================================

def assign_risk(probability):

    if probability >= 70:
        return "High Risk"

    elif probability >= 40:
        return "Medium Risk"

    else:
        return "Low Risk"


results["Risk_Level"] = results[
    "Churn_Probability"
].apply(assign_risk)


# ============================================================
# 20. SAVE PREDICTIONS
# ============================================================

output_folder = "data/processed"

os.makedirs(
    output_folder,
    exist_ok=True
)

prediction_file = (
    f"{output_folder}/churn_predictions.csv"
)

results.to_csv(
    prediction_file,
    index=False
)


# ============================================================
# 21. RISK SUMMARY
# ============================================================

print("\n===== RISK SUMMARY =====")

print(
    results["Risk_Level"].value_counts()
)


# ============================================================
# 22. SAVE MODEL METRICS
# ============================================================

metrics = pd.DataFrame(
    {
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC-AUC"
        ],
        "Value": [
            accuracy,
            precision,
            recall,
            f1,
            roc_auc
        ]
    }
)

metrics_file = (
    f"{output_folder}/model_metrics.csv"
)

metrics.to_csv(
    metrics_file,
    index=False
)


# ============================================================
# 23. FINAL OUTPUT
# ============================================================

print("\n============================================================")
print("MODEL COMPLETE")
print("============================================================")

print("Prediction file:")
print(prediction_file)

print("\nMetrics file:")
print(metrics_file)

print("\nTotal predictions:", len(results))

print("\nRetainIQ ML pipeline completed successfully.")
print("============================================================")