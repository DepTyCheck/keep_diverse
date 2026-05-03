# exp007 — legacy filtration wall-clock on 50 files (sv vs otk)

Counterpart to `tsdm_experiments/exp000_timing_50/`. Runs one legacy
`keep_diverse` filtration round on each of two 50-file datasets and prints
`elapsed_seconds` for each, so the wall-clock cost of legacy filtration can be
compared across datasets of very different per-file sizes.

Datasets (referenced via symlinks):

- `data/`     → `tests/data_50` (sv, ~2 KB/file)
- `data_otk/` → `experiments/exp005_box_plot_pct_rnd_otk/data/otk` (otk, ~45 KB/file)

Run:

```bash
python -m experiments.exp007_timing_50_legacy.do_experiment
```
