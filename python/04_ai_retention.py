import pandas as pd
import os

# ============================================================
# RETAINIQ - AI RETENTION INTELLIGENCE
# ============================================================

print("\n============================================================")
print("RETAINIQ - AI RETENTION INTELLIGENCE")
print("============================================================")


# ============================================================
# 1. LOAD ML PREDICTIONS
# ============================================================

input_file = "data/processed/churn_predictions.csv"

print("\n===== LOADING CHURN PREDICTIONS =====")

df = pd.read_csv(input_file)

print("Prediction data loaded successfully.")
print("Customers:", len(df))


# ============================================================
# 2. CREATE RETENTION RECOMMENDATION FUNCTION
# ============================================================

def generate_recommendation(row):

    reasons = []
    actions = []

    # --------------------------------------------------------
    # CONTRACT
    # --------------------------------------------------------

    contract = str(row.get("Contract", "")).lower()

    if "month-to-month" in contract:
        reasons.append("month-to-month contract")
        actions.append("offer a longer-term contract with an incentive")

    # --------------------------------------------------------
    # TENURE
    # --------------------------------------------------------

    try:
        tenure = float(row.get("Tenure_Months", 0))
    except:
        tenure = 0

    if tenure <= 6:
        reasons.append("short customer tenure")
        actions.append("provide an onboarding and loyalty offer")

    elif tenure <= 12:
        reasons.append("relatively short tenure")
        actions.append("offer a loyalty benefit to encourage renewal")

    # --------------------------------------------------------
    # INTERNET SERVICE
    # --------------------------------------------------------

    internet = str(
        row.get("Internet_Service", "")
    ).lower()

    if "fiber" in internet:
        reasons.append("fiber optic internet service")
        actions.append("review pricing and service experience for fiber customers")

    # --------------------------------------------------------
    # TECH SUPPORT
    # --------------------------------------------------------

    tech_support = str(
        row.get("Tech_Support", "")
    ).lower()

    if tech_support in ["no", "no internet service"]:
        reasons.append("no technical support subscription")
        actions.append("offer a technical support package")

    # --------------------------------------------------------
    # ONLINE SECURITY
    # --------------------------------------------------------

    security = str(
        row.get("Online_Security", "")
    ).lower()

    if security in ["no", "no internet service"]:
        reasons.append("no online security subscription")
        actions.append("offer an online security package")

    # --------------------------------------------------------
    # MONTHLY CHARGES
    # --------------------------------------------------------

    try:
        monthly_charges = float(
            row.get("Monthly_Charges", 0)
        )
    except:
        monthly_charges = 0

    if monthly_charges >= 80:
        reasons.append("high monthly charges")
        actions.append("offer a personalized pricing or bundle review")

    # --------------------------------------------------------
    # PAPERLESS BILLING
    # --------------------------------------------------------

    paperless = str(
        row.get("Paperless_Billing", "")
    ).lower()

    if paperless == "yes":
        reasons.append("paperless billing")
        actions.append("review billing communication and payment experience")

    # --------------------------------------------------------
    # PAYMENT METHOD
    # --------------------------------------------------------

    payment = str(
        row.get("Payment_Method", "")
    ).lower()

    if "electronic check" in payment:
        reasons.append("electronic check payment method")
        actions.append("offer easier automatic payment options")

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if not reasons:
        reasons.append("multiple customer behavior signals")
        actions.append("review customer account and offer personalized retention support")

    return (
        "; ".join(reasons),
        "; ".join(actions)
    )


# ============================================================
# 3. GENERATE AI-STYLE INSIGHTS
# ============================================================

print("\n===== GENERATING RETENTION INSIGHTS =====")

results = df.apply(
    generate_recommendation,
    axis=1
)

df["Key_Risk_Factors"] = [
    result[0]
    for result in results
]

df["Recommended_Action"] = [
    result[1]
    for result in results
]


# ============================================================
# 4. CREATE CUSTOMER SEGMENT
# ============================================================

def create_segment(row):

    try:
        probability = float(
            row["Churn_Probability"]
        )
    except:
        probability = 0

    contract = str(
        row.get("Contract", "")
    ).lower()

    try:
        monthly = float(
            row.get("Monthly_Charges", 0)
        )
    except:
        monthly = 0

    if probability >= 70 and (
        "month-to-month" in contract
        or monthly >= 80
    ):
        return "Critical Retention"

    elif probability >= 70:
        return "High Risk"

    elif probability >= 40:
        return "Watchlist"

    else:
        return "Stable"


df["Customer_Segment"] = df.apply(
    create_segment,
    axis=1
)


# ============================================================
# 5. RETENTION PRIORITY
# ============================================================

def retention_priority(segment):

    if segment == "Critical Retention":
        return 1

    elif segment == "High Risk":
        return 2

    elif segment == "Watchlist":
        return 3

    else:
        return 4


df["Retention_Priority"] = df[
    "Customer_Segment"
].apply(retention_priority)


# ============================================================
# 6. SORT CUSTOMERS
# ============================================================

df = df.sort_values(
    by=[
        "Retention_Priority",
        "Churn_Probability"
    ],
    ascending=[
        True,
        False
    ]
)


# ============================================================
# 7. SAVE AI OUTPUT
# ============================================================

output_folder = "data/processed"

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = (
    f"{output_folder}/ai_retention_recommendations.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 8. DISPLAY SUMMARY
# ============================================================

print("\n===== CUSTOMER SEGMENTS =====")

print(
    df["Customer_Segment"].value_counts()
)


# ============================================================
# 9. DISPLAY TOP HIGH-RISK CUSTOMERS
# ============================================================

print("\n===== TOP 10 RETENTION PRIORITIES =====")

columns_to_display = [
    "Churn_Probability",
    "Risk_Level",
    "Customer_Segment",
    "Key_Risk_Factors",
    "Recommended_Action"
]

available_columns = [
    column
    for column in columns_to_display
    if column in df.columns
]

print(
    df[available_columns].head(10).to_string(
        index=False
    )
)


# ============================================================
# 10. FINAL MESSAGE
# ============================================================

print("\n============================================================")
print("AI RETENTION INTELLIGENCE COMPLETE")
print("============================================================")

print("\nOutput file:")
print(output_file)

print("\nTotal customers analyzed:", len(df))

print("\nRetainIQ AI layer completed successfully.")
print("============================================================")