import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

def clean_data(input_path, output_path, fill_method, normalize_method, outlier_method,
               encode_method, drop_duplicates, duplicate_cols, strip_whitespace,
               validate_cols, report_path, logger, normalize_cols=None, encode_cols=None, outlier_cols=None):


    # --- Load Data ---
    df = pd.read_csv(input_path)
    original_shape = df.shape
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    auto_categoricals = df.select_dtypes(include=['object', 'category']).columns.tolist()
    auto_categoricals += [
        col for col in df.select_dtypes(include='number').columns
        if df[col].nunique() < 10
    ]
    auto_categoricals = list(set(auto_categoricals))

    auto_numerics = [
        col for col in df.select_dtypes(include='number').columns
        if col not in auto_categoricals
    ]

    encode_targets = [col.strip() for col in encode_cols.split(',')] if encode_cols else auto_categoricals
    normalize_targets = [col.strip() for col in normalize_cols.split(',')] if normalize_cols else auto_numerics

    report_lines = []
    report_lines.append("# 📊 Data Cleaning Report")
    report_lines.append(f"- **Run time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"- **Input file:** `{input_path}`")
    report_lines.append(f"- **Output file:** `{output_path}`\n")

    report_lines.append("## 📐 Initial Dataset")
    report_lines.append(f"- Rows: {original_shape[0]}")
    report_lines.append(f"- Columns: {original_shape[1]}\n")

    logger.info(f"Loaded data with shape: {original_shape}")

    # --- Strip Whitespace ---
    if strip_whitespace:
        stripped = []
        for col in df.select_dtypes(include=['object', 'category']):
            df[col] = df[col].astype(str).str.strip()
            stripped.append(col)
            logger.info(f"Stripped whitespace from column: {col}")
        if stripped:
            report_lines.append("## 🔠 Whitespace Cleanup")
            report_lines.append(f"- Stripped whitespace from: `{', '.join(stripped)}`\n")

    # --- Fill Missing Values ---
    if fill_method:
        report_lines.append("## 🔧 Missing Value Filling")
        report_lines.append(f"- Method: `{fill_method}`")
        for col in df.select_dtypes(include=np.number).columns:
            if df[col].isnull().sum() > 0:
                if fill_method == 'mean':
                    val = df[col].mean()
                elif fill_method == 'median':
                    val = df[col].median()
                elif fill_method == 'mode':
                    val = df[col].mode()[0]
                df[col] = df[col].fillna(val)
                logger.info(f"Filled missing values in '{col}' with {val}")
                report_lines.append(f"  - `{col}` → filled with `{val}`")
        report_lines.append("")

    # --- Remove Duplicates ---
    if drop_duplicates:
        before = df.shape[0]
        if duplicate_cols:
            subset_cols = [col.strip() for col in duplicate_cols.split(',')]
            df = df.drop_duplicates(subset=subset_cols)
            logger.info(f"Removed duplicates using columns: {subset_cols}")
            report_lines.append("## 🧹 Duplicate Removal")
            report_lines.append(f"- Based on columns: `{', '.join(subset_cols)}`")
        else:
            df = df.drop_duplicates()
            logger.info("Removed full row duplicates")
            report_lines.append("## 🧹 Duplicate Removal")
            report_lines.append("- Based on full rows")
        removed = before - df.shape[0]
        report_lines.append(f"- Duplicates removed: `{removed}`\n")

    if outlier_method:
        report_lines.append("## 🧪 Outlier Removal")
        report_lines.append(f"- Method: `{outlier_method}`")

        outlier_targets = [col.strip() for col in outlier_cols.split(',')] if outlier_cols else auto_numerics
        outlier_mask = pd.Series(False, index=df.index)

        for col in outlier_targets:
            if col not in df.columns:
                logger.warning(f"Outlier column '{col}' not found in DataFrame.")
                continue

            if outlier_method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                col_mask = ~df[col].between(lower, upper)
            elif outlier_method == 'zscore':
                std = df[col].std()
                if std == 0 or np.isnan(std):
                    logger.warning(f"Skipped outlier detection for column '{col}' due to zero or NaN std.")
                    continue
                z_scores = (df[col] - df[col].mean()) / std
                col_mask = z_scores.abs() > 3
            else:
                logger.warning(f"Unknown outlier method: {outlier_method}")
                continue

            outlier_mask |= col_mask.fillna(False)
            removed = col_mask.sum()
            logger.info(f"Marked {removed} outliers from '{col}'")
            report_lines.append(f"  - `{col}` → `{removed}` outliers marked")

        total_removed = outlier_mask.sum()
        df = df[~outlier_mask]
        logger.info(f"Total outliers removed: {total_removed}")
        report_lines.append(f"- **Total outlier rows removed:** `{total_removed}`\n")

        # --- Encode Categoricals ---
    if encode_method:
        report_lines.append("## 🔣 Categorical Encoding")
        report_lines.append(f"- Method: `{encode_method}`")

        for col in encode_targets:
            if encode_method == 'label':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                logger.info(f"Label encoded column '{col}'")
                report_lines.append(f"  - `{col}` encoded (label)")

            elif encode_method == 'onehot':
                onehot = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df.drop(columns=[col]), onehot], axis=1)
                logger.info(f"Applied one-hot encoding to: {col}")
                report_lines.append(f"  - `{col}` encoded (one-hot)")
    # --- Normalize ---
    if normalize_method:
        report_lines.append("## 📊 Normalization")
        report_lines.append(f"- Method: `{normalize_method}`")

        for col in normalize_targets:
            if col not in df.columns:
                continue
            if normalize_method == 'zscore':
                mean = df[col].mean()
                std = df[col].std()
                df[col] = (df[col] - mean) / std
                logger.info(f"Z-score normalized '{col}' (mean={mean}, std={std})")
                report_lines.append(f"  - `{col}` normalized (z-score)")

            elif normalize_method == 'minmax':
                min_val = df[col].min()
                max_val = df[col].max()
                df[col] = (df[col] - min_val) / (max_val - min_val)
                logger.info(f"Min-max scaled '{col}' (min={min_val}, max={max_val})")
                report_lines.append(f"  - `{col}` normalized (min-max)")
        report_lines.append("")

    # --- Validate Columns ---
    if validate_cols:
        report_lines.append("## ⚠️ Column Validation Warnings")
        for col in df.columns:
            if df[col].nunique(dropna=False) == 1:
                logger.warning(f"Column '{col}' is constant")
                report_lines.append(f"- `{col}` is constant")
            if df[col].isnull().mean() == 1.0:
                logger.warning(f"Column '{col}' is entirely null")
                report_lines.append(f"- `{col}` is entirely null")
            if df[col].dtype == 'object' and df[col].nunique() / len(df) > 0.5:
                logger.warning(f"Column '{col}' has high cardinality")
                report_lines.append(f"- `{col}` has high cardinality")
        report_lines.append("")

    # --- Save Output CSV ---
    df.to_csv(output_path, index=False)
    logger.info(f"Saved cleaned data to {output_path}")

    # --- Final Dataset Shape ---
    report_lines.append("## 📉 Final Dataset Shape")
    report_lines.append(f"- Rows: {df.shape[0]}")
    report_lines.append(f"- Columns: {df.shape[1]}")

    # --- Write Markdown Report ---
    if report_path:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        logger.info(f"Saved report to {report_path}")

