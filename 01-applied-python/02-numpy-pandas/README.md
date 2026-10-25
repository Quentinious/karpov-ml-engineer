# NumPy and Pandas

## Array operations

`numpy-array-operations.ipynb` implements a scalar product, column-wise min-max
scaling, cosine similarity, IQR outlier detection, a regularized matrix inverse,
column-median imputation and one-hot encoding. It demonstrates axes, broadcasting,
boolean masks, missing values and linear algebra. The regularized inverse is a
matrix operation; this notebook does not train or evaluate a regression model.

The timing cell allocates 100 million Python integers and is intended for separate
manual execution. The duplicate timing syntax was removed and NumPy is imported
before its use in annotations. Zero ranges, zero vector norms, all-NaN columns
and singular matrices remain numerical edge cases to review. Demonstration lists
need conversion to arrays before calling array-specific functions.

## Application data analysis

`playstore-analysis.ipynb` explores application records, counts missing ratings,
selects rows and columns, removes duplicate names, normalizes column names,
calculates free/paid shares, filters educational applications and converts prices.
It then summarizes mean price, rating and review count by category and app type.
Concepts: DataFrame indexing, concatenation, string methods, type conversion,
relative frequencies, pivot tables and CSV export.

Place an authorized copy of `playstore.csv` beside the notebook and start Jupyter
in this directory. That input is absent; the included
`playstore-category-summary.csv` is a 63-row aggregate whose schema and displayed
values match the saved pivot output, not a replacement for the raw input.
The original notebook and dataset provenance still need confirmation.

Saved outputs were inspected for credentials and retained as historical results;
they were not regenerated. The notebook still exports `5_result.csv` and
`11_result.csv`; these generated outputs are ignored by Git.

Stack: Python, Jupyter/IPython, NumPy and Pandas. These dependencies are separate
from the API and Airflow environments. The original environment versions were
not recorded, so exact reproduction is not yet verified.
