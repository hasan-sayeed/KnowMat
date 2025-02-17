[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
<!-- These are examples of badges you might also want to add to your README. Update the URLs accordingly.
[![Built Status](https://api.cirrus-ci.com/github/<USER>/KnowMat.svg?branch=main)](https://cirrus-ci.com/github/<USER>/KnowMat)
[![ReadTheDocs](https://readthedocs.org/projects/KnowMat/badge/?version=latest)](https://KnowMat.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/KnowMat/main.svg)](https://coveralls.io/r/<USER>/KnowMat)
[![PyPI-Server](https://img.shields.io/pypi/v/KnowMat.svg)](https://pypi.org/project/KnowMat/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/KnowMat.svg)](https://anaconda.org/conda-forge/KnowMat)
[![Monthly Downloads](https://pepy.tech/badge/KnowMat/month)](https://pepy.tech/project/KnowMat)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/KnowMat)
-->

# **KnowMat**: Transforming Complexity into Clarity

Figure: Schematic of the KnowMat LLM pipeline for extracting structured materials data from unstructured literature.

## Overview

**KnowMat** KnowMat is an easy-to-use Flask-based web application that implements a lightweight LLM pipeline for extracting structured, machine-readable materials data from unstructured scientific literature. Built using Ollama, KnowMat streamlines the process of parsing PDFs, extracting key information—such as composition, processing conditions, characterization details, and performance properties—and saving the results in CSV format. This CSV output can then be used to build or extend a database for further analysis or machine learning applications.

This system is designed to run on consumer-grade computers, making advanced data extraction accessible without requiring high-end hardware.

## Features

- **Automated Data Extraction**: Parse PDFs and extract material compositions, processing conditions, characterization, and performance properties.

- **User-Friendly Web App**: A Flask-based interface that is simple to use yet powerful.

- **Model Selection**: Supports multiple open-source models via Ollama.
CSV Output: Easily save extraction results as a CSV file, enabling you to build or extend an existing database.

- **Multiple File Upload**: Upload several PDFs at once and extend your database incrementally across sessions.

## Installation

### Prerequisites

1. **Ollama**:

   Visit [Ollama](https://ollama.com/) to download and install the Ollama client. Launch Ollama and ensure it is running in the background.

2. **Conda**:

   Make sure Conda is installed on your system.

### Steps

1. Clone the Repository:

   ```bash
   git clone https://github.com/hasan-sayeed/KnowMat.git
   cd KnowMat
   ```

2. Create and Activate the Conda Environment:

   ```bash
   conda env create -f environment.yml
   conda activate KnowMat
   ```

3. Pull the Required Models from Ollama:

   ```bash
   ollama pull <model_name>
   ```

   - For **Llama 3.1 8B Instruct** (medium in size ~16GB with high accuracy), use:

      `llama3.1:8b-instruct-fp16` as <model_name>

   - For a lighter (6.4GB) and faster model, use:

      `llama3.2:3b-instruct-fp16`

   - For users with strong hardware who want state-of-the-art performance, try:

      `llama3.3:70b-instruct-fp16`

   (Note: Llama 3.3 70B offers similar performance to the Llama 3.1 405B model but is huge in size, approximately 141GB.)

4. Run the Web Application:

   ```bash
   python src/knowmat/knowmat_web_app.py
   ```

5. Open the App:

   Open your browser and navigate to

   ```bash
   http://127.0.0.1:5000.
   ```


## Usage

- **Model Selection:**

   On the left pane of the web app, choose your preferred model from the dropdown menu. **Before choosing a model, make sure you have pulled the required model from Ollama following the instructions above.**

- **File Upload:**

   You can upload multiple PDF files at once using the file uploader in the sidebar.

- **CSV Output:**

   Specify the output folder path and the CSV file name where the extracted data will be saved. If you use the same path and CSV file name in multiple sessions, KnowMat will append the new extraction results to your existing database, allowing you to extend your dataset over time.

- **View Results:**

   The right pane displays the extracted data for each PDF one by one as soon as extraction for that file is completed.


## Project Organization

```
├── AUTHORS.md              <- List of developers and maintainers.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Guidelines for contributing to this project.
├── Dockerfile              <- Build a docker container with `docker build .`.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yml         <- The conda environment file for reproducibility.
├── models                  <- Trained and serialized models, model predictions,
│                              or model summaries.
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for
│                              ordering), the creator's initials and a description,
│                              e.g. `1.0-fw-initial-data-exploration`.
├── pyproject.toml          <- Build configuration. Don't change! Use `pip install -e .`
│                              to install for development or to build `tox -e build`.
├── references              <- Data dictionaries, manuals, and all other materials.
├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures             <- Generated plots and figures for reports.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── setup.py                <- [DEPRECATED] Use `python setup.py develop` to install for
│                              development or `python setup.py bdist_wheel` to build.
├── src
│   └── knowmat             <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `pytest`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
├── .isort.cfg              <- Configuration for git hook that sorts imports.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

## 🚀 Future Enhancements

- [ ] **Additional Model Support**: Expand the list of supported models and allow for custom model integration.

- [ ] **Advanced Post-Processing**: Further refine extraction accuracy using additional custom prompts and techniques.

- [ ] **Enhanced UI/UX**: Improve the Flask web interface for a more seamless and responsive user experience.

- [ ] **Evaluation of Extracted Outputs**: Integrate evaluation metrics into the pipeline to assess the quality and accuracy of the extracted data, ensuring robust performance in real-world applications.

## Feedback

We truly value your input and are excited to hear your feedback and suggestions! If you have any ideas for improvements, feature requests, or if you encounter any issues, please feel free to open an issue on our GitHub repository. We're always eager to collaborate, so if you're interested in contributing, reach out to our developers. Your insights help us make KnowMat even better!

<!-- pyscaffold-notes -->

## Note

This project has been set up using [PyScaffold] 4.6 and the [dsproject extension] 0.7.2.

[conda]: https://docs.conda.io/
[pre-commit]: https://pre-commit.com/
[Jupyter]: https://jupyter.org/
[nbstripout]: https://github.com/kynan/nbstripout
[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[PyScaffold]: https://pyscaffold.org/
[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject
