import pandas as pd
import mysql.connector

# ============================================================
# RETAINIQ - CLEAN MYSQL IMPORT
# ============================================================

CSV_PATH = "data/processed/telco_churn_cleaned.csv"

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DATABASE = "RetainIQ"
TABLE = "customers"


# ============================================================
# 1. READ CSV
# ============================================================

print("\nLoading CSV...")

df = pd.read_csv(
    CSV_PATH,
    dtype=str,
    keep_default_na=False
)

print("CSV loaded.")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ============================================================
# 2. FIX COLUMN NAME
# ============================================================

df.rename(
    columns={"Count": "Count_Value"},
    inplace=True
)


# ============================================================
# 3. CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)

cursor = connection.cursor()

print("Connected.")


# ============================================================
# 4. SELECT DATABASE
# ============================================================

cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DATABASE}`")
cursor.execute(f"USE `{DATABASE}`")


# ============================================================
# 5. DELETE OLD TABLE
# ============================================================

cursor.execute(f"DROP TABLE IF EXISTS `{TABLE}`")


# ============================================================
# 6. CREATE TABLE AUTOMATICALLY
# ============================================================

columns = []

for column in df.columns:
    columns.append(f"`{column}` TEXT")

create_table_sql = f"""
CREATE TABLE `{TABLE}` (
    {", ".join(columns)}
)
"""

cursor.execute(create_table_sql)

print("Table created.")


# ============================================================
# 7. INSERT DATA
# ============================================================

column_names = ", ".join(
    f"`{column}`"
    for column in df.columns
)

placeholders = ", ".join(
    ["%s"] * len(df.columns)
)

insert_sql = f"""
INSERT INTO `{TABLE}`
({column_names})
VALUES ({placeholders})
"""


print("\nImporting data...")

data = [
    tuple(row)
    for row in df.itertuples(index=False, name=None)
]

cursor.executemany(insert_sql, data)

connection.commit()


# ============================================================
# 8. VERIFY
# ============================================================

cursor.execute(
    f"SELECT COUNT(*) FROM `{TABLE}`"
)

total = cursor.fetchone()[0]


print("\n================================")
print("RETAINIQ IMPORT COMPLETE")
print("================================")
print("CSV rows:", len(df))
print("MySQL rows:", total)
print("================================")


# ============================================================
# 9. CLOSE
# ============================================================

cursor.close()
connection.close()