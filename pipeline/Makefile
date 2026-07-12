# One-command reproduction. `make smoke` runs anywhere (numpy only);
# `make hero` runs in Claude Science / a full env (see environment.yml).
PY ?= python3
DATA ?= data/ShifrutMarson2018.h5ad
CONTROL ?= NT

RANKED ?= outputs_gladstone/ranked_perturbations.csv

.PHONY: smoke synthetic hero direction figure env lock
smoke:            ## dependency-free unit tests: E-distance core + signed direction axis + figure
	$(PY) edistance_core.py
	$(PY) direction.py
	$(PY) direction_figure.py

synthetic:        ## end-to-end on a tiny synthetic AnnData (needs anndata+scanpy)
	$(PY) run_pipeline.py --synthetic --outdir outputs_synth

direction:        ## genome-scale signed direction axis (needs scanpy + the built h5ad; see direction_genomescale.py)
	$(PY) direction_genomescale.py --data $(DATA) --lib $(LIB) --control $(CONTROL) --out outputs_gladstone/direction_scores_raw.csv --meta outputs_gladstone/direction_meta.json
	$(PY) merge_direction.py --ranked $(RANKED) --direction outputs_gladstone/direction_scores_raw.csv --out $(RANKED)

figure:           ## render the hero signed-causal-map figure from the merged leaderboard
	$(PY) figure_causal_map.py --ranked $(RANKED)
	$(PY) figure_targets.py
	$(PY) figure_evidence.py

hero:             ## full pipeline on real data -> outputs/ranked_perturbations.csv
	$(PY) run_pipeline.py --data $(DATA) --control $(CONTROL) --outdir outputs

env:              ## create the conda environment
	conda env create -f environment.yml || conda env update -f environment.yml

lock:             ## pin exact versions after first successful run
	conda env export --no-builds > lock.yml
