# Wiring the DGX Spark into Claude Science (remote GPU over SSH)

**Goal:** run the genome-scale scVI + Perturb-seq analysis on your **NVIDIA DGX Spark** (GB10 Grace-Blackwell) instead of Modal — free, local, 128 GB unified memory, Blackwell GPU. Claude Science drives it over SSH; the laptop just orchestrates.

## The key facts (researched)
- **Claude Science supports plain workstations over SSH — no Slurm required.** Per the docs: *"Workstations run jobs as detached processes. SLURM clusters receive jobs via `sbatch`."* A single-node Spark is a **workstation host**, so my earlier "you may need Slurm" caveat was wrong — you don't. ([Claude Science: remote compute](https://claude.com/docs/claude-science/remote-compute-clusters))
- Claude Science **uses your `~/.ssh/config`**, authenticates with your key / `ssh-agent`, and **installs nothing** on the Spark. Adding a host runs a **read-only probe** recording CPUs, memory, **GPUs + CUDA driver**, conda/modules/Apptainer, scratch dirs, and whether `sbatch` exists.
- **Jobs run outside the sandbox, as your user on the Spark** — full access to what your account can read/write there. Jobs survive disconnects; default timeout **30 min** (tell Claude before longer work); outputs pulled back, files >~100 MB stay on the host with paths recorded.
- **DGX Spark = ARM64 (aarch64)**: 20-core Arm (10× Cortex-X925 + 10× A725), Blackwell GPU (6144 CUDA cores), 128 GB unified LPDDR5x, **DGX OS = Ubuntu 24.04 + CUDA**. ([NVIDIA DGX Spark hardware](https://docs.nvidia.com/dgx/dgx-spark/hardware.html), [system overview](https://docs.nvidia.com/dgx/dgx-spark/system-overview.html)). The ARM architecture is the one thing that changes the environment build (below).

## Prerequisites (on your side, once)
1. **SSH reachability + key auth.** From the laptop, `ssh spark` should log in without a password (key or `ssh-agent`). If it prompts for a password, set up key auth first.
2. **A `~/.ssh/config` Host block** for the Spark, e.g.:
   ```
   Host spark
       HostName 192.168.x.x        # or the Spark's hostname / Tailscale name
       User <you>
       IdentityFile ~/.ssh/id_ed25519
   ```
   *(This is the block I asked you to paste — I use only Host/HostName/User, never the key.)*
3. **Scratch space** on the Spark with room for the data + scVI checkpoints, e.g. `/home/<you>/cs-scratch` or a fast NVMe path.

## Setup in Claude Science (the part in the app)
1. **Settings → Compute → SSH hosts → Add SSH host.**
2. Choose/type the alias **`spark`** (address/user/port/ProxyJump come from `~/.ssh/config`).
3. In **notes**, tell Claude about the host up front (it reads these before the first job) — paste the **Host Details** block below.
4. Click **Add** → it runs the probe (should detect the Blackwell GPU + CUDA, and **no `sbatch` → treated as a workstation**).
5. On the host's detail page set **Scratch root** (your `cs-scratch` path) and a **Concurrent job limit** (e.g. 4).

### Host Details notes to paste (accurate for the Spark)
```
Architecture: ARM64 (aarch64), DGX OS (Ubuntu 24.04) + CUDA (Blackwell GB10 GPU), 128 GB unified memory.
Scheduler: none — single-node workstation. Run jobs as detached processes (no sbatch).
Environments: use conda/mamba with aarch64 (linux-aarch64) builds. For scvi-tools, install PyTorch with
  CUDA for ARM (NVIDIA sbsa build or conda-forge pytorch-gpu aarch64) — NOT the x86 wheel. scanpy/anndata/
  pertpy/pydeseq2 are all available for aarch64 via conda-forge.
Data: stage datasets under <scratch>/data. Long jobs (scVI training) take >30 min — raise the timeout.
Unified memory: the 128 GB is shared CPU+GPU, so large AnnData + scVI fit without a separate VRAM ceiling.
```

## The ARM64 gotcha (the only real friction)
`scvi-tools` needs **PyTorch built for aarch64 + CUDA**. On the Spark, the reliable path is a fresh conda/mamba env with `linux-aarch64` packages; install PyTorch from NVIDIA's ARM CUDA channel (or `conda-forge` `pytorch-gpu`). scanpy/pertpy/pydeseq2/pydeseq2 install cleanly for aarch64. Put this instruction in Host Details so Claude Science builds the right env on first run. (NVIDIA's [DGX Spark Porting Guide](https://docs.nvidia.com/dgx/dgx-spark-porting-guide/overview.html) and [Anaconda's DGX Spark notes](https://www.anaconda.com/blog/python-nvidia-dgx-spark-first-impressions) cover ARM Python specifics.)

## The genome-scale run, on the Spark
Once the host is added, tell Claude Science (one message) to run on it:
1. On `spark` scratch: download the genome-scale primary-T-cell Perturb-seq (or Schmidt GSE190604 fallback).
2. `single-cell-rna-qc` skill for QC.
3. `scvi-tools` skill: train scVI/scANVI on the **Blackwell GPU** (donor = batch key) → `X_scVI`; subsample ~300 cells/perturbation first.
4. `python run_pipeline.py --data <file> --control <label> --modality <detected> --embedding X_scVI --max-cells-per-group 300 --outdir outputs` (the pipeline already accepts `--embedding` + the memory cap).
5. Pull `outputs/ranked_perturbations.csv` back to `~/Claude Hackathon/pipeline/outputs/` → my results-watcher + I take over for enrichment.
**Raise the job timeout** before the scVI step (it's the long one).

## Security note (worth knowing)
Remote jobs run **as you, outside any sandbox**, on the Spark — they can read/write anything your account can. That's expected for your own box; just be aware it's not sandboxed like the local runs.

## Sources
[Claude Science remote compute](https://claude.com/docs/claude-science/remote-compute-clusters) · [Claude Science compute providers](https://claude.com/docs/claude-science/compute-providers) · [DGX Spark hardware](https://docs.nvidia.com/dgx/dgx-spark/hardware.html) · [DGX Spark system overview](https://docs.nvidia.com/dgx/dgx-spark/system-overview.html) · [DGX Spark porting guide](https://docs.nvidia.com/dgx/dgx-spark-porting-guide/overview.html) · [Anaconda: Python on DGX Spark](https://www.anaconda.com/blog/python-nvidia-dgx-spark-first-impressions)
