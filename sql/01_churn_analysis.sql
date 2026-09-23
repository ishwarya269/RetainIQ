-- ============================================================
-- RETAINIQ
-- Customer Retention & Churn Intelligence
-- SQL Analysis
-- ============================================================


-- ============================================================
-- 1. CREATE DATABASE
-- ============================================================

CREATE DATABASE IF NOT EXISTS RetainIQ;

USE RetainIQ;
 drop table if exists customers;


-- ============================================================
-- 2. CREATE CUSTOMER TABLE
-- ============================================================

CREATE TABLE customers (
    CustomerID VARCHAR(50),
    Count_Value INT,
    Country VARCHAR(100),
    State VARCHAR(100),
    City VARCHAR(100),
    Zip_Code VARCHAR(20),
    Lat_Long VARCHAR(100),
    Latitude DECIMAL(10,6),
    Longitude DECIMAL(10,6),
    Gender VARCHAR(20),
    Senior_Citizen INT,
    Partner VARCHAR(20),
    Dependents VARCHAR(20),
    Tenure_Months INT,
    Phone_Service VARCHAR(20),
    Multiple_Lines VARCHAR(50),
    Internet_Service VARCHAR(50),
    Online_Security VARCHAR(50),
    Online_Backup VARCHAR(50),
    Device_Protection VARCHAR(50),
    Tech_Support VARCHAR(50),
    Streaming_TV VARCHAR(50),
    Streaming_Movies VARCHAR(50),
    Contract VARCHAR(50),
    Paperless_Billing VARCHAR(20),
    Payment_Method VARCHAR(100),
    Monthly_Charges DECIMAL(10,2),
    Total_Charges DECIMAL(10,2),
    Churn_Label VARCHAR(20),
    Churn_Value INT,
    Churn_Score INT,
    CLTV DECIMAL(10,2),
    Churn_Reason VARCHAR(255)
);


-- ============================================================
-- 3. VERIFY TABLE
-- ============================================================

DESCRIBE customers;


-- ============================================================
-- 4. BASIC DATA ANALYSIS
-- ============================================================

-- Total customers
SELECT
    COUNT(*) AS total_customers
FROM customers;


-- Total churned customers
SELECT
    COUNT(*) AS churned_customers
FROM customers
WHERE Churn_Value = 1;


-- Total retained customers
SELECT
    COUNT(*) AS retained_customers
FROM customers
WHERE Churn_Value = 0;


-- ============================================================
-- 5. OVERALL CHURN RATE
-- ============================================================

SELECT
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers;


-- ============================================================
-- 6. CHURN BY CONTRACT TYPE
-- ============================================================

SELECT
    Contract,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Contract
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 7. CHURN BY INTERNET SERVICE
-- ============================================================

SELECT
    Internet_Service,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Internet_Service
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 8. CHURN BY PAYMENT METHOD
-- ============================================================

SELECT
    Payment_Method,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Payment_Method
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 9. CHURN BY GENDER
-- ============================================================

SELECT
    Gender,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Gender
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 10. CHURN BY SENIOR CITIZEN STATUS
-- ============================================================

SELECT
    Senior_Citizen,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Senior_Citizen
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 11. CHURN BY TENURE GROUP
-- ============================================================

SELECT
    CASE
        WHEN Tenure_Months <= 6 THEN '0-6 Months'
        WHEN Tenure_Months <= 12 THEN '7-12 Months'
        WHEN Tenure_Months <= 24 THEN '13-24 Months'
        WHEN Tenure_Months <= 48 THEN '25-48 Months'
        ELSE '49+ Months'
    END AS tenure_group,

    COUNT(*) AS total_customers,

    SUM(Churn_Value) AS churned_customers,

    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage

FROM customers

GROUP BY
    CASE
        WHEN Tenure_Months <= 6 THEN '0-6 Months'
        WHEN Tenure_Months <= 12 THEN '7-12 Months'
        WHEN Tenure_Months <= 24 THEN '13-24 Months'
        WHEN Tenure_Months <= 48 THEN '25-48 Months'
        ELSE '49+ Months'
    END

ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 12. MONTHLY CHARGES VS CHURN
-- ============================================================

SELECT
    Churn_Label,
    COUNT(*) AS customers,
    ROUND(AVG(Monthly_Charges), 2) AS average_monthly_charges,
    ROUND(AVG(Total_Charges), 2) AS average_total_charges
FROM customers
GROUP BY Churn_Label;


-- ============================================================
-- 13. CHURN BY PAPERLESS BILLING
-- ============================================================

SELECT
    Paperless_Billing,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Paperless_Billing
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 14. CHURN BY TECH SUPPORT
-- ============================================================

SELECT
    Tech_Support,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Tech_Support
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 15. CHURN BY ONLINE SECURITY
-- ============================================================

SELECT
    Online_Security,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Online_Security
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 16. HIGH-RISK CUSTOMERS
-- ============================================================

SELECT
    CustomerID,
    Tenure_Months,
    Contract,
    Internet_Service,
    Monthly_Charges,
    Total_Charges,
    Churn_Score,
    CLTV,
    Churn_Label
FROM customers
WHERE Churn_Value = 1
ORDER BY Churn_Score DESC
LIMIT 20;


-- ============================================================
-- 17. HIGH-VALUE CHURNED CUSTOMERS
-- ============================================================

SELECT
    CustomerID,
    Contract,
    Tenure_Months,
    Monthly_Charges,
    Total_Charges,
    Churn_Score,
    CLTV,
    Churn_Reason
FROM customers
WHERE Churn_Value = 1
ORDER BY CLTV DESC
LIMIT 20;


-- ============================================================
-- 18. COMMON CHURN REASONS
-- ============================================================

SELECT
    Churn_Reason,
    COUNT(*) AS number_of_customers
FROM customers
WHERE Churn_Value = 1
  AND Churn_Reason IS NOT NULL
  AND Churn_Reason <> ''
GROUP BY Churn_Reason
ORDER BY number_of_customers DESC;


-- ============================================================
-- 19. CHURN BY CONTRACT + INTERNET SERVICE
-- ============================================================

SELECT
    Contract,
    Internet_Service,
    COUNT(*) AS total_customers,
    SUM(Churn_Value) AS churned_customers,
    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS churn_rate_percentage
FROM customers
GROUP BY Contract, Internet_Service
ORDER BY churn_rate_percentage DESC;


-- ============================================================
-- 20. FINAL BUSINESS SUMMARY
-- ============================================================

SELECT

    COUNT(*) AS total_customers,

    SUM(Churn_Value) AS total_churned,

    COUNT(*) - SUM(Churn_Value) AS total_retained,

    ROUND(
        SUM(Churn_Value) * 100.0 / COUNT(*),
        2
    ) AS overall_churn_rate,

    ROUND(AVG(Monthly_Charges), 2)
        AS average_monthly_charges,

    ROUND(AVG(Total_Charges), 2)
        AS average_total_charges,

    ROUND(AVG(Tenure_Months), 2)
        AS average_tenure_months

FROM customers;