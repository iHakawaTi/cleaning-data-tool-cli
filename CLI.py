# Import libraries
import argparse  # Handles parsing command-line arguments
from cleaner.core import clean_data  # Main data-cleaning logic
from cleaner.logger import setup_logger  # Logging system
import pandas as pd
import numpy as np


def main():
    parser = argparse.ArgumentParser(description="Clean messy CSV files.")

    parser.add_argument('--input', required=True, help='Path to input CSV file')
    parser.add_argument('--output', help='Path to output CSV file')  # no longer required
    parser.add_argument('--log', default='logs/clean_run.log', help='Log file path')
    parser.add_argument('--fill-missing', choices=['mean', 'median', 'mode'], default='mean')
    parser.add_argument('--normalize', choices=['zscore', 'minmax'], default=None)
    parser.add_argument('--remove-outliers', choices=['zscore', 'iqr'], default=None)
    parser.add_argument('--profile', action='store_true', help='Show a summary of the input dataset')
    parser.add_argument('--encode-categoricals', choices=['label', 'onehot'], help='Encode categorical columns using "label" or "onehot"')
    parser.add_argument('--drop-duplicates', action='store_true', help='Remove duplicate rows from the dataset')
    parser.add_argument('--duplicate-cols', help='Comma-separated column names to check for duplicates (default: all columns)')
    parser.add_argument('--strip-whitespace', action='store_true', help='Strip whitespace from string columns')
    parser.add_argument('--validate-cols', action='store_true', help='Check for common column issues')
    parser.add_argument('--report', help='Path to write a Markdown report with dataset summary')
    parser.add_argument('--normalize-cols', type=str,
                        help='Comma-separated list of numeric columns to normalize (overrides auto)')
    parser.add_argument('--encode-cols', type=str,
                        help='Comma-separated list of categorical columns to encode (overrides auto)')
    parser.add_argument('--outlier-cols', type=str, default=None,
                        help='Columns to apply outlier removal to, comma-separated')

    args = parser.parse_args()
    logger = setup_logger(args.log)

    # ✅ Bypass output requirement for --profile
    if args.profile:
        df = pd.read_csv(args.input)
        logger.info(f"Dataset shape: {df.shape}")
        logger.info("\nColumn types:\n" + str(df.dtypes))
        logger.info("\nNull values per column:\n" + str(df.isnull().sum()))

        numeric_cols = df.select_dtypes(include=np.number)
        stats = numeric_cols.describe().transpose()
        logger.info("\nNumeric column summary:\n" + str(stats))

        print("📊 Dataset Profile:")
        print(f"Shape: {df.shape}")
        print("\nColumn types:")
        print(df.dtypes)
        print("\nNull values:")
        print(df.isnull().sum())
        print("\nStats (numeric columns):")
        print(stats)
        return  # ✅ exit here after profiling

    # ❗ If not profiling, then output is required
    if not args.output:
        parser.error("--output is required unless using --profile")

    # 🧼 Now run the actual data cleaner
    clean_data(
        input_path=args.input,
        output_path=args.output,
        fill_method=args.fill_missing,
        normalize_method=args.normalize,
        outlier_method=args.remove_outliers,
        encode_method=args.encode_categoricals,
        drop_duplicates=args.drop_duplicates,
        duplicate_cols=args.duplicate_cols,
        strip_whitespace=args.strip_whitespace,
        validate_cols=args.validate_cols,
        report_path=args.report,
        logger=logger,
        normalize_cols=args.normalize_cols,
        encode_cols=args.encode_cols,
        outlier_cols=args.outlier_cols
    )


# Ensure this runs only when executed directly (not imported)
if __name__ == '__main__':
    main()
