# 📊 Data Cleaning Report
- **Run time:** 2025-05-31 18:02:59
- **Input file:** `data\Dataset of Diabetes .csv`
- **Output file:** `data/Dataset of Diabetes _cleaned.csv`

## 📐 Initial Dataset
- Rows: 1000
- Columns: 14

## 🔠 Whitespace Cleanup
- Stripped whitespace from: `Gender, CLASS`

## 🔧 Missing Value Filling
- Method: `mean`

## 🧹 Duplicate Removal
- Based on columns: `ID`
- Duplicates removed: `200`

## 🧪 Outlier Removal
- Method: `zscore`
  - `AGE` → `2` outliers marked
- **Total outlier rows removed:** `2`

## 🔣 Categorical Encoding
- Method: `onehot`
  - `Gender` encoded (one-hot)
  - `CLASS` encoded (one-hot)
## ⚠️ Column Validation Warnings

## 📉 Final Dataset Shape
- Rows: 798
- Columns: 17