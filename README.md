# Poisson Difference-in-Differences (Poisson DiD) Tutorial
## Causal Inference on Hotel Demand under Wildfire Shocks

This repository contains an educational tutorial on **Poisson Difference-in-Differences (Poisson DiD)**, a modern econometric methodology for causal inference on count and sparse data. The tutorial uses a real-world case study: the impact of the historic **June 2017 Portuguese Mega-Wildfires** on resort hotel booking demand, leveraging the famous **Hotel Booking Demand Dataset**.

---

## 🌟 Overview

Difference-in-Differences (DiD) is widely used in economics and data science to estimate treatment effects. However, when the outcome variable is a count (e.g., weekly booking counts) or has a **mass of zeros**, standard Ordinary Least Squares (OLS) models fail:
1. **Negative Predictions**: Linear regressions predict negative counts (e.g., $-2.4$ bookings), which are physically impossible.
2. **The $\log(Y + \epsilon)$ Landmine**: Transforming the target variable using $\log(Y + \epsilon)$ to handle zeros introduces severe specification bias. Changing the arbitrary constant $\epsilon$ shifts the treatment effect coefficients, standard errors, and statistical significance.

### 🔍 Case Study Context & Intuition
* **The Primary Causal Outcome (Booking Demand)**: While cancellations are interesting, the primary economic shock is on **overall booking demand (total bookings/arrivals)**. A major wildfire causes booking demand to collapse dramatically at resorts in the affected region.
* **The Counter-Intuitive Cancellations Drop**: A common assumption is that a disaster like a wildfire should *increase* cancellations. However, this study shows that the wildfires caused group cancellations to drop to **absolute zero** at the resort. This occurred because the wildfire caused a complete collapse in overall booking demand (no new bookings were made for the summer/autumn arrival weeks). Because guests cannot cancel reservations that were never made, cancellations fell to absolute zero.
* **Pre-Wildfire Spikes & Seasonal Lows**: The large peaks before the wildfire represent seasonal business-cycle fluctuations of lumpy group bookings. Furthermore, beach resorts naturally experience group bookings dropping to near-zero during peak summer months (July–September) because they prioritize high-margin individual leisure tourists over discounted group tours (yield management).
* **Threat to Parallel Trends & Causal Proof**: Because the resort and city hotels have different seasonal profiles, this seasonal difference threatens the Parallel Trends assumption of DiD. However, while group bookings normally rebound strongly in October (autumn convention/tour season), post-wildfire (October 2017) bookings stayed at absolute zero. This failure to rebound in autumn confirms a persistent causal shock rather than a normal seasonal cycle.

In this tutorial, we estimate Poisson DiD models for both **overall demand (total bookings)** and **cancellations** to illustrate this entire economic mechanism, placing demand at the center of our analysis.

**Poisson DiD** solves this by using an exponential link function and a log link, modeling **Multiplicative Parallel Trends** instead of linear parallel trends. It naturally accommodates zeros, restricts predictions to non-negative numbers, and estimates the **Incidence Rate Ratio (IRR)** directly.

---

## 📊 Model Estimation Results

Below is a summary of the causal estimation results for weekly group booking demand (`total_bookings`) across the three models implemented in this tutorial:

| Model Specification | Outcome Variable | Causal Parameter ($\theta$) | Std. Error | P-Value | Causal Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Standard OLS DiD** | `total_bookings` | $+10.5000$ | $33.090$ | $0.751$ | $+10.5$ bookings/week change (statistically insignificant) |
| **2. Poisson DiD (PPML)** | `total_bookings` | $-2.4290$ | $0.839$ | $0.004$ | $-91.19\%$ change in rate of bookings (statistically significant) |
| **3. ETWFE Poisson DiD** | `total_bookings` | $-0.8597$ | $0.795$ | $0.280$ | $-0.86$ bookings/week change (statistically insignificant) |

* **OLS fails to identify the shock**: The linear OLS model estimates a positive but highly noisy coefficient ($+10.5$) with a standard error ($33.09$) that is three times larger than the estimate. It completely fails to capture the collapse in demand because it struggles with the large seasonal spikes and mass of zeros.
* **Poisson DiD reveals the true effect**: By modeling the exponential link natively, Poisson DiD handles the zeroes and yields a statistically significant causal coefficient of $-2.4290$. This corresponds to an Incidence Rate Ratio (IRR) of $0.0881$, or a **$91.19\%$ drop in booking demand** directly attributable to the wildfire.
* **ETWFE Saturated Poisson validates the shock**: When we expand to a multi-unit panel and control for heterogeneous treatment effects using Wooldridge's saturated cohort-time interaction estimator (corrected for cohort specification), we obtain an aggregated causal effect of **$-0.86$ bookings/week** ($p = 0.280$), indicating that the relative trend in group booking demand did not differ significantly between Resort and City hotels for the Online TA segment.

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
