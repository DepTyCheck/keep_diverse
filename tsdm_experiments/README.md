# TSDm experiments

Experiments targeting the TSDm filter (`tsdm_src/`, `tsdm_main.py`),
parallel to the eps-based experiments under `experiments/`.

Datasets are referenced via symlinks — no file copies.

## Running

Each experiment is a stand-alone script:

```bash
python tsdm_experiments/exp000_timing_50/do_experiment.py
python tsdm_experiments/exp001_subjective_vs_subjective/do_experiment.py
python -m tsdm_experiments.exp002_big.do_experiment
python tsdm_experiments/exp006_tsdm_kept_counts/do_experiment.py
```

Outputs land under each experiment's `output/` directory (gitignored).
