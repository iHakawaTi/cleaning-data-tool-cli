import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import os
import streamlit as st
import zipfile

def load_templates(path="templates.json"):
    with open(path, "r") as f:
        return json.load(f)

def profile_summary(df):
    st.markdown("### 🔍 Profile Summary")
    st.write("**Shape:**", df.shape)
    st.write("**Column Types:**", df.dtypes)
    st.write("**Missing Values:**")
    st.write(df.isnull().sum())
    st.write("**Descriptive Stats:**")
    st.write(df.describe())

def generate_visuals(df):
    st.markdown("### 📊 Data Visualizations")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        st.subheader("Boxplot for Outlier Detection")
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.boxplot(data=df[numeric_cols], ax=ax)
        st.pyplot(fig)

def create_zip(output_csv, report_md, log_txt, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        if os.path.exists(output_csv):
            zipf.write(output_csv)
        if os.path.exists(report_md):
            zipf.write(report_md)
        if os.path.exists(log_txt):
            zipf.write(log_txt)
