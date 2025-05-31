# 🧼 Cleaning-Data-Tool-CLI

A powerful **CLI + GUI tool** for automated data cleaning, profiling, and exploratory data analysis — built with Python, Pandas, and Streamlit.

---

## 🚀 Features

| Feature                | Description                                    |
|------------------------|------------------------------------------------|
| ✅ Fill missing values  | mean, median, mode strategies                  |
| ✅ Remove outliers      | using Z-score or IQR                           |
| ✅ Normalize values     | Z-score and MinMax scaling                     |
| ✅ Encode categoricals  | Label or One-Hot Encoding                      |
| ✅ Strip whitespace     | Clean string columns                           |
| ✅ Drop duplicates      | Based on all or selected columns               |
| ✅ Visual EDA           | Boxplots, histograms, correlation, bar charts |
| ✅ Validation checks    | Constant cols, full-null, high-cardinality     |
| ✅ Reports & logs       | Markdown report and .log file saved            |
| ✅ GUI Mode             | Built with Streamlit                           |
| ✅ CLI Mode             | For scripting and automation                   |

---

## 📦 Project Structure

```
cleaning-data-tool-cli/
│
├── CLI.py                 # Command-line interface
├── GUI.py                 # Streamlit GUI
├── cleaner/               # Core logic (clean_data)
│   ├── core.py
│   ├── logger.py
│   └── utils.py
│
├── data/                  # Input/output CSVs (gitignored)
├── reports/               # Markdown reports
├── logs/                  # Log files
├── tests/                 # Unit tests
├── requirements.txt       # Dependencies
├── templates.json         # (optional) presets for GUI
└── README.md              # This file
```

---

## 🧪 CLI Usage

### ✅ Multi-line Example (Linux/macOS/Bash)
```bash
python CLI.py \
  --input "data/input.csv" \
  --output "data/cleaned.csv" \
  --fill-missing mean \
  --normalize zscore \
  --remove-outliers iqr \
  --normalize-cols "Glucose,BloodPressure,BMI" \
  --outlier-cols "Glucose,BloodPressure,Insulin,BMI" \
  --encode-categoricals label \
  --drop-duplicates \
  --duplicate-cols "Pregnancies,Glucose,BloodPressure" \
  --strip-whitespace \
  --validate-cols \
  --report "reports/cleaning_report.md"
```

### ✅ One-liner (Windows/PowerShell)

```bash
python CLI.py --input "data/input.csv" --output "data/cleaned.csv" --fill-missing mean --normalize zscore --remove-outliers iqr --normalize-cols "Glucose,BloodPressure,BMI" --outlier-cols "Glucose,BloodPressure,Insulin,BMI" --encode-categoricals label --drop-duplicates --duplicate-cols "Pregnancies,Glucose,BloodPressure" --strip-whitespace --validate-cols --report "reports/cleaning_report.md"
```

---

## 🖥 GUI Mode (Streamlit)

### 🔧 Launch the GUI

```bash
streamlit run GUI.py
```

### 🎛 GUI Features

- Upload CSV files
- Configure cleaning options interactively
- Visualizations:
  - Boxplots
  - Histograms
  - Correlation Heatmap
  - Category bar charts
- View cleaned data in tabs
- Download cleaned CSV, Markdown report, and logs
- Export everything as a ZIP bundle

---

## 🧪 Run Tests

```bash
python -m pytest tests/
```

---

## 📥 Output Files

After cleaning, you will find:

```
data/
  cleaned.csv
  your_cleaned_file_bundle.zip

logs/
  cleaning_run.log

reports/
  cleaning_report.md
```

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

Contributions welcome!  
If you find bugs or have ideas, feel free to open an issue or pull request.
