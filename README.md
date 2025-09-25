# Scottish Income Tax (NSND) — 2025/26

A simple Streamlit app that calculates **Scottish Income Tax** for **non-savings, non-dividend** income,
applying the UK **Personal Allowance** (including taper above £100k), and shows a band-by-band breakdown.

## 🧮 What it does
- Computes **Personal Allowance** (PA £12,570; taper £1 per £2 above £100,000; £0 by £125,140).
- Applies Scottish bands (Starter, Basic, Intermediate, Higher, Advanced, Top) to **taxable income**.
- Presents a **table** and **chart** of tax by band, plus effective tax rate.

> Scope: NSND income only. Excludes savings/dividends (UK-wide rates), NI, student loans, and other reliefs.

## 🚀 Run locally

```bash
# 1) clone
git clone https://github.com/<your-username>/scottish-income-tax-app.git
cd scottish-income-tax-app

# 2) create env (optional)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3) install
pip install -r requirements.txt

# 4) run
streamlit run app.py
