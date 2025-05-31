import pandas as pd
import logging
from cleaner.core import clean_data


def test_fill_mean(tmp_path):
    # Create a sample DataFrame with missing values
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [4, 5, 6]
    })

    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"

    df.to_csv(input_file, index=False)

    clean_data(
        input_path=str(input_file),
        output_path=str(output_file),
        fill_method="mean",
        normalize_method=None,
        outlier_method=None,
        encode_method=None,
        drop_duplicates=False,
        duplicate_cols=None,
        strip_whitespace=False,
        validate_cols=False,
        report_path=None,
        logger=logging.getLogger(),
        normalize_cols=None,
        encode_cols=None,
        outlier_cols=None
    )

    result = pd.read_csv(output_file)

    # Check that there are no missing values in column A
    assert result["A"].isnull().sum() == 0

def test_outlier_removal(tmp_path):
    import logging
    from cleaner.core import clean_data
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3, 1000]})  # one obvious outlier
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    df.to_csv(input_file, index=False)

    clean_data(
        input_path=str(input_file),
        output_path=str(output_file),
        fill_method=None,
        normalize_method=None,
        outlier_method="iqr",
        encode_method=None,
        drop_duplicates=False,
        duplicate_cols=None,
        strip_whitespace=False,
        validate_cols=False,
        report_path=None,
        logger=logging.getLogger(),
        normalize_cols=None,
        encode_cols=None,
        outlier_cols="A"
    )

    result = pd.read_csv(output_file)
    # make sure the outlier was removed
    assert result["A"].max() < 1000
def test_label_encoding(tmp_path):
    import pandas as pd
    import logging
    from cleaner.core import clean_data

    df = pd.DataFrame({"Gender": ["Male", " Female", "Female", " Male"]})  # dirty spaces
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    df.to_csv(input_file, index=False)

    clean_data(
        input_path=str(input_file),
        output_path=str(output_file),
        fill_method=None,
        normalize_method=None,
        outlier_method=None,
        encode_method="label",
        drop_duplicates=False,
        duplicate_cols=None,
        strip_whitespace=True,  # 💥 Turned on!
        validate_cols=False,
        report_path=None,
        logger=logging.getLogger(),
        normalize_cols=None,
        encode_cols="Gender",
        outlier_cols=None
    )

    result = pd.read_csv(output_file)
    print(result)
    print(result.dtypes)

    assert result["Gender"].isin([0, 1]).all()
