import streamlit as st
import pandas as pd
import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns

from cleaner.core import clean_data
from cleaner.utils import profile_summary, generate_visuals, create_zip

st.set_page_config(page_title="Data Cleaning Tool", layout="wide")
st.title("🧼 Cleaning-Data-Tool-CLI (Streamlit GUI)")
st.markdown("Upload a CSV, explore it visually, clean it flexibly, and download results.")

# Upload
uploaded_file = st.file_uploader("📁 Upload your CSV file", type=["csv"])

if uploaded_file:
    os.makedirs("data", exist_ok=True)
    input_path = os.path.join("data", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    base_name = os.path.splitext(uploaded_file.name)[0]
    output_path = f"data/{base_name}_cleaned.csv"
    report_path = f"reports/{base_name}_report.md"
    log_path = f"logs/{base_name}.log"
    zip_path = f"data/{base_name}_bundle.zip"

    df = pd.read_csv(input_path)
    st.write("📊 Preview of Uploaded Data", df.head())
    st.info(f"🔢 Rows: {df.shape[0]} | Columns: {df.shape[1]}")

    if os.path.exists(output_path):
        st.warning(f"⚠️ Output file `{output_path}` will be overwritten.")

    # Optional profile
    if st.checkbox("🔍 Show Dataset Profile Only (No Cleaning)"):
        profile_summary(df)
        st.stop()

    # Cleaning Config
    with st.form("cleaning_form"):
        st.subheader("⚙️ Cleaning Configuration")

        fill_method = st.selectbox("Fill Missing Values", ["None", "mean", "median", "mode"], index=0)
        outlier_method = st.selectbox("Remove Outliers", ["None", "zscore", "iqr"], index=0)
        normalize_method = st.selectbox("Normalize Numeric Columns", ["None", "minmax", "zscore"], index=0)
        encoding_method = st.selectbox("Encode Categorical Columns", ["None", "label", "onehot"], index=0)

        duplicate_cols = st.multiselect("Columns to Check for Duplicates", df.columns)
        normalize_cols = st.multiselect("Columns to Normalize", df.select_dtypes(include="number").columns)
        encode_cols = st.multiselect("Columns to Encode", df.select_dtypes(include="object").columns)
        outlier_cols = st.multiselect("Columns for Outlier Removal", df.select_dtypes(include="number").columns)

        drop_dupes = st.checkbox("Drop Duplicates", value=True)
        strip_ws = st.checkbox("Strip Whitespace", value=True)
        validate = st.checkbox("Validate Columns", value=True)

        submit = st.form_submit_button("🧼 Run Cleaning")

    # Run cleaning
    if submit:
        st.subheader("🔄 Cleaning in Progress...")
        os.makedirs("logs", exist_ok=True)
        os.makedirs("reports", exist_ok=True)

        logger = logging.getLogger(base_name)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
        handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

        try:
            clean_data(
                input_path=input_path,
                output_path=output_path,
                fill_method=fill_method.lower() if fill_method != "None" else None,
                normalize_method=normalize_method.lower() if normalize_method != "None" else None,
                outlier_method=outlier_method.lower() if outlier_method != "None" else None,
                encode_method=encoding_method.lower() if encoding_method != "None" else None,
                drop_duplicates=drop_dupes,
                duplicate_cols=",".join(duplicate_cols) if duplicate_cols else None,
                strip_whitespace=strip_ws,
                validate_cols=validate,
                report_path=report_path,
                logger=logger,
                normalize_cols=",".join(normalize_cols) if normalize_cols else None,
                encode_cols=",".join(encode_cols) if encode_cols else None,
                outlier_cols=",".join(outlier_cols) if outlier_cols else None,
            )

            cleaned_df = pd.read_csv(output_path)
            st.session_state["cleaned_df"] = cleaned_df
            st.session_state["original_shape"] = df.shape

            st.success("✅ Data cleaned successfully!")
            st.info(f"📉 Rows reduced: {df.shape[0]} → {cleaned_df.shape[0]} | Columns: {cleaned_df.shape[1]}")

        except Exception as e:
            st.error(f"❌ Cleaning failed due to: {e}")

    # Show results and visuals
    if "cleaned_df" in st.session_state:
        cleaned_df = st.session_state["cleaned_df"]
        orig_shape = st.session_state["original_shape"]
        removed_rows = orig_shape[0] - cleaned_df.shape[0]
        row_drop_pct = (removed_rows / orig_shape[0]) * 100 if orig_shape[0] else 0

        st.subheader("📊 Results and Visuals")
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Cleaned Data", "📈 Visuals", "🧾 Report & Logs", "📦 Download All"])

        with tab1:
            st.dataframe(cleaned_df.head())
            st.metric("Rows Removed", f"{removed_rows} ({row_drop_pct:.2f}%)")
            with open(output_path, "rb") as f:
                st.download_button("📥 Download Cleaned CSV", f, file_name=os.path.basename(output_path), mime="text/csv")

        with tab2:
            st.markdown("### 📈 Select Visual Type")
            viz_type = st.selectbox("Choose a visualization", ["Boxplot", "Histogram", "Correlation Heatmap", "Categorical Barplot"])

            if viz_type == "Boxplot":
                numeric_cols = cleaned_df.select_dtypes(include="number").columns
                if len(numeric_cols) > 0:
                    fig, ax = plt.subplots(figsize=(10, 5))
                    sns.boxplot(data=cleaned_df[numeric_cols], ax=ax)
                    ax.set_title("Boxplot of Numeric Columns")
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
                    st.pyplot(fig)
                else:
                    st.info("No numeric columns available for boxplot.")

            elif viz_type == "Histogram":
                numeric_cols = cleaned_df.select_dtypes(include="number").columns
                selected = st.multiselect("Select numeric columns", numeric_cols)
                for col in selected:
                    fig, ax = plt.subplots()
                    sns.histplot(cleaned_df[col], kde=True, ax=ax)
                    ax.set_title(f"Histogram of {col}")
                    st.pyplot(fig)

            elif viz_type == "Correlation Heatmap":
                numeric_cols = cleaned_df.select_dtypes(include="number").columns
                if len(numeric_cols) >= 2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sns.heatmap(cleaned_df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
                    st.pyplot(fig)
                else:
                    st.info("Not enough numeric columns to generate heatmap.")

            elif viz_type == "Categorical Barplot":
                cat_cols = cleaned_df.select_dtypes(include=["object", "category"]).columns
                selected = st.multiselect("Select categorical columns", cat_cols)
                for col in selected:
                    fig, ax = plt.subplots()
                    cleaned_df[col].value_counts().plot(kind="bar", ax=ax)
                    ax.set_title(f"Value Counts for {col}")
                    st.pyplot(fig)

        with tab3:
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    st.subheader("🧾 Cleaning Report")
                    st.markdown(f.read())
            else:
                st.warning("⚠️ Report not found.")

            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    st.subheader("📚 Cleaning Log")
                    st.text(f.read())
            else:
                st.warning("⚠️ Log not found.")

        with tab4:
            create_zip(output_path, report_path, log_path, zip_path)
            with open(zip_path, "rb") as f:
                st.download_button("📦 Download ZIP Bundle", f, file_name=os.path.basename(zip_path), mime="application/zip")
