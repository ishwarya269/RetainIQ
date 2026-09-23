import pandas as pd
import os

# ============================================================
# RETAINIQ - DATA CLEANING
# ============================================================

# 1. LOAD RAW DATASET
file_path = "data/raw/Telco_customer_churn.xlsx"

print("\n===== LOADING DATASET =====")

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")


# ============================================================
# 2. DATASET OVERVIEW
# ============================================================

print("\n===== DATASET OVERVIEW =====")

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumn names:")
for column in df.columns:
    print("-", repr(column))


# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", "_", regex=True)
)

print("\n===== CLEANED COLUMN NAMES =====")

for column in df.columns:
    print("-", repr(column))


# ============================================================
# 4. REMOVE DUPLICATE ROWS
# ============================================================

duplicates = df.duplicated().sum()

print("\nDuplicate rows found:", duplicates)

df = df.drop_duplicates()

print("Duplicate rows removed.")


# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

print("\n===== MISSING VALUES =====")

missing_values = df.isnull().sum()

print(missing_values)


# ============================================================
# 6. DISPLAY DATA TYPES
# ============================================================

print("\n===== DATA TYPES =====")

print(df.dtypes)


# ============================================================
# 7. BASIC STATISTICS
# ============================================================

print("\n===== BASIC STATISTICS =====")

print(df.describe(include="all"))


# ============================================================
# 8. CREATE PROCESSED FOLDER IF NEEDED
# ============================================================

processed_folder = "data/processed"

os.makedirs(processed_folder, exist_ok=True)


# ============================================================
# 9. SAVE CLEANED DATASET
# ============================================================

output_path = "data/processed/telco_churn_cleaned.csv"

df.to_csv(output_path, index=False)

print("\n===== SUCCESS =====")

print("Cleaned dataset saved successfully!")
print("Location:", output_path)

print("\nFinal rows:", df.shape[0])
print("Final columns:", df.shape[1])