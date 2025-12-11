# Keep Diverse

`keep_diverse` is a utility designed to filter a collection of text files to get a diverse subset. It performs pairwise NCD comparisons between files and, based on a chosen metric, identifies files that should be removed.

## Usage

Run the tool using `main.py`:

```bash
git clone https://github.com/DepTyCheck/keep_diverse.git
cd keep_diverse
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --dir /path/to/text/files --kept-files /path/to/output/kept_files.txt
```

### Required Arguments

- `--dir`: Path to the directory containing the text files you want to filter
- `--kept-files`: Path where the list of filtered (kept) files will be saved

### Optional Arguments

#### Output & Reporting
- `--filtration-plot`: Path to save a visualization plot of the filtration process
- `--counter-report`: Path to save a detailed JSON report of file removal counters

#### Execution Control
- `--max-files`: Limit the maximum number of files to read from the input directory
- `--processes-count`: Number of parallel processes to use for filtration (default: 10).
Set this to `1` if you need to avoid out-of-memory issues
- `--filter-rounds`: Number of filtration rounds to perform
- `--stop-pct`: Percentage threshold to stop filtration early if convergence is detected (default: 0.03)

#### Algorithm Parameters
- `--split-by`: Internal parameter for splitting data chunks (default: 50)
- `--relative-eps`: Relative epsilon for finding percentage thresholds (default: 0.00001)
- `--max-tries-to-find-pct`: Maximum attempts to find percentage thresholds (default: 10)
- `--min-indices-count`: Minimum number of files to keep for a subset (default: 10)

## Installation

You can install it as a python package:

```bash
pip install git+https://github.com/DepTyCheck/keep_diverse@master
```
