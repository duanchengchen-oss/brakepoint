# One-command reproduction. `make smoke` runs anywhere (numpy only);
# `make hero` runs in Claude Science / a full env (see environment.yml).
PY ?= python3
DATA ?= data/ShifrutMarson2018.h5ad
CONTROL ?= NT

.PHONY: smoke synthetic hero env lock
smoke:            ## dependency-free unit test of the E-distance core (CI-safe)
	$(PY) edistance_core.py

synthetic:        ## end-to-end on a tiny synthetic AnnData (needs anndata+scanpy)
	$(PY) run_pipeline.py --synthetic --outdir outputs_synth

hero:             ## full pipeline on real data -> outputs/ranked_perturbations.csv
	$(PY) run_pipeline.py --data $(DATA) --control $(CONTROL) --outdir outputs

env:              ## create the conda environment
	conda env create -f environment.yml || conda env update -f environment.yml

lock:             ## pin exact versions after first successful run
	conda env export --no-builds > lock.yml
