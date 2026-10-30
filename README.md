# CCIS 727 Assignment 7 — CLIP prompt comparison

**Execution status:** implementation prepared; the current cloud proxy blocks the official CIFAR-10 and CLIP weight downloads with `403 Forbidden`. No accuracy measurements or experimental conclusions are claimed. The notebook retains the failed execution output. The included `report.pdf` is an explicitly incomplete draft covering the conceptual questions; its experimental section remains pending. A successful notebook run replaces it with a measured-results report.

## Reproduce

Use Python 3.12 on Linux. From this checkout:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_notebook.py
```

The runner executes `assignment7.ipynb` from the repository root and saves outputs even if a cell fails. It exits nonzero on failure. The `python3` kernel must use the installed environment (the bundled native ipykernel uses the runner's interpreter). Open the saved notebook in a notebook viewer; the headless runner does not require a Jupyter web server.

The first run needs HTTPS access to GitHub, PyPI, the PyTorch wheel index, `www.cs.toronto.edu`, its redirect host `www.cs.utoronto.ca`, and `openaipublic.azureedge.net`. Keep TLS and dataset/checkpoint checksum verification enabled. The cloud configuration draft includes the three additional dataset/weight domains, but they have not yet been applied to the running instance.

## Fixed experiment

- Official CIFAR-10 **test** split; 100 images, 10/class, without replacement; seed **42**. NumPy `default_rng` samples each class in official class order and sorts indices within class before concatenation. Selection precedes inference and is saved verbatim.
- Official class order: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck.
- A: `{class}`. B: `a photo of a {class}.` No prompt changes after evaluation.
- Official OpenAI **ViT-B/32**, source revision `d05afc436d78f1c48dc0dbf8e5980a9d471f35f6`; official pretrained checkpoint, no training or fine-tuning. The notebook records the checkpoint SHA-256 after CLIP verifies it.
- Official `clip.tokenize` and supplied preprocessing: bicubic resize/center crop to 224, RGB conversion, tensor conversion, CLIP normalization (mean 0.48145466/0.4578275/0.40821073; standard deviation 0.26862954/0.26130258/0.27577711).
- Frozen image/text encoders, evaluation mode, no gradients. Batch size **16**; image embeddings computed once. Normalize 512-dimensional embeddings, multiply image/text matrices, choose largest cosine. No softmax or learned logit scaling.
- Hardware available: AMD EPYC 9V74 CPU, 5 logical CPUs, approximately 33 GiB RAM; no GPU. Notebook uses at most 4 CPU threads. CUDA is used only if available in another compatible installation.
- Python **3.12.14**, torch **2.5.1+cpu**, torchvision **0.20.1+cpu**, CLIP **1.0** at the pinned revision, NumPy **2.2.6**, pandas **2.2.3**, matplotlib **3.10.3**, scikit-learn **1.6.1**, nbformat **5.10.4**, nbclient **0.10.2**, ipykernel **6.29.5**, ReportLab **4.4.1**, Pillow **13.0.0**. All dependencies are pinned in `requirements.txt`.

## Outputs after successful execution

`assignment7.ipynb` contains the displayed examples, both full 100×10 score matrices, embedding shapes and numerical cosine example, accuracy tables, confusion matrices, paired counts, and five-image comparison. `report.pdf` is generated from those measured results and addresses Section 5 with course-reading references.

The `outputs/` directory receives:

- `selected_indices.csv`: sample order, original test index, true class ID/name.
- `predictions.csv`: true class, A/B predictions, A/B correctness, top cosine and prediction-change flag for each image.
- `scores_A.csv`, `scores_B.csv`: class cosine scores, with two identifying columns preceding the ten class columns.
- `accuracy_comparison.csv`, `per_class_accuracy.csv` and `summary.json`: measured accuracies, paired counts, configuration and runtime metadata.
- `class_examples.png`, `confusion_A.png`, `confusion_B.png`, `five_image_analysis.png` and `five_image_analysis.csv`.

Five examples prioritize changed predictions with errors, then other errors, with correct fillers only if needed. These are the identical five input images for both conditions. Cosines are similarities, not calibrated probabilities. The fixed test sample is not used for prompt tuning. Small sample size, 32×32 source resolution, and unknown pretraining overlap limit conclusions.

Do not submit `data/`, `.cache/` or the virtual environment; they are ignored. An accessible repository containing the same deliverables is accepted by the assignment instead of a ZIP.

## Sources and attribution

- [OpenAI CLIP](https://github.com/openai/CLIP/tree/d05afc436d78f1c48dc0dbf8e5980a9d471f35f6) (MIT): model loading, preprocessing, tokenization, encoding and normalized dot-product scoring are adapted from its documented zero-shot examples. [Radford et al., 2021](https://proceedings.mlr.press/v139/radford21a.html).
- [Official CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html), Krizhevsky (2009); loaded using torchvision's CIFAR10 dataset with `train=False`.
- Course reading, *Vision Language Models.pdf* (dated August 14, 2025): “CLIP” (PDF pp. 1–2), “Dynamic Resolution” (p. 4), “VLM Architectures” (pp. 4–5), “Cross Attention Adapter” (p. 5), “MLP Adapter” (p. 6). The supplied PDF is cited but not redistributed.
- [Liu et al., Visual Instruction Tuning, 2023](https://arxiv.org/abs/2304.08485), for the conceptual LLaVA comparison only.
