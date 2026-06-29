# Poisson Difference-in-Differences (Poisson DiD) Tutorial

This repository contains an educational tutorial on **Poisson Difference-in-Differences (Poisson DiD)**, a modern econometric methodology for causal inference on count and sparse data. The tutorial uses a real-world case study: the impact of the historic **June 2017 Portuguese Mega-Wildfires** on resort hotel cancellations, leveraging the famous **Hotel Booking Demand Dataset**.

---

## 🌟 Overview

Difference-in-Differences (DiD) is widely used in economics and data science to estimate treatment effects. However, when the outcome variable is a count (e.g., weekly cancellations) or has a **mass of zeros**, standard Ordinary Least Squares (OLS) models fail:
1. **Negative Predictions**: Linear regressions predict negative counts (e.g., $-2.4$ cancellations), which are physically impossible.
2. **The $\log(Y + \epsilon)$ Landmine**: Transforming the target variable using $\log(Y + \epsilon)$ to handle zeros introduces severe specification bias. Changing the arbitrary constant $\epsilon$ shifts the treatment effect coefficients, standard errors, and statistical significance.

**Poisson DiD** solves this by using an exponential link function and a log link, modeling **Multiplicative Parallel Trends** instead of linear parallel trends. It naturally accommodates zeros, restricts predictions to non-negative numbers, and estimates the **Incidence Rate Ratio (IRR)** directly.

---

## 📂 Project Structure

```text
├── data/
│   └── hotels.csv                 # Raw dataset (Downloaded automatically)
├── src/
│   └── data_loader.py             # Data processing and panel construction
├── utils/
│   └── plotting.py                 # Premium data visualizations
├── poisson_did_tutorial.ipynb     # Interactive Jupyter Notebook tutorial
├── pyproject.toml                 # uv project configuration
└── README.md                      # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

You need `uv` installed for fast, modern package management. If you don't have it, install it via:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. Clone the repository and navigate to the project directory:
   ```bash
   cd hotel-cancellations-and-mega-wildfires
   ```
2. Sync the virtual environment and install all dependencies:
   ```bash
   uv sync
   ```
3. Start the Jupyter Notebook environment:
   ```bash
   uv run jupyter notebook
   ```
   Open `poisson_did_tutorial.ipynb` to step through the analysis.

   > [!TIP]
   > The project environment has been registered as a Jupyter kernel. In your Jupyter interface or VS Code, select the kernel named **Python (hotel-cancellations-did)**.


---

## 🔬 Core Methodologies Covered

- **Standard Linear DiD**: Baseline OLS regression with negative predictions.
- **Log-linear DiD Sensitivity Analysis**: Empirical proof of the $\log(Y + \epsilon)$ landmine.
- **Poisson Pseudo-Maximum Likelihood (PPML)**: Classic Poisson regression with robust standard errors (`statsmodels`).
- **Extended Two-Way Fixed Effects (ETWFE)**: Modern Wooldridge (2023) saturated cohort-time interaction models (`etwfe`).
- **Diagnostics**: Trends testing (`diff-diff`).

---

## 📚 References
- Antonio, N., de Almeida, A., & Nunes, L. (2019). *Hotel Booking Demand Datasets*. Data in Brief, 22, 219–225.
- Wooldridge, J. M. (2023). *Simple approaches to nonlinear difference-in-differences with panel data*. Journal of Econometrics, 235(2), 2215-2239.
- Roth, J., Sant’Anna, P. H., Bilinski, A., & Poe, J. (2023). *What’s trending in difference-in-differences? A synthesis of the recent econometrics literature*. Journal of Econometrics, 235(2), 2218-2244.
