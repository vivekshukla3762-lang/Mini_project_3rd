# Mini_project_3rd
# 🛡️ Malicious URL Detector

A machine-learning project that classifies URLs as **safe** or **malicious/phishing** using only the structure of the URL itself. It ships with a training script and an interactive [Streamlit](https://streamlit.io) web app for checking links one at a time or in bulk.

> The detector never visits the link. It only analyses the URL text, so it is safe to test suspicious URLs.

## Features

- **25 handcrafted URL features**: length, dots/hyphens/digits, IP address as host, `@` symbol, HTTPS, subdomain count, suspicious keywords (`login`, `verify`, ...), brand names in subdomains, risky TLDs, URL shorteners, entropy, percent-encoding, and more.
- **Two models compared automatically**: Logistic Regression and Random Forest. The one with the best test accuracy is saved to `model.joblib`.
- **Interactive UI** with three tabs:
  - **Single URL**: risk score, verdict (safe / suspicious / malicious), plain-English red flags, extracted features, and top model features.
  - **Batch**: upload a CSV of URLs, get scored results, and download them.
  - **Model info**: model type and feature list.
- **Stdlib-only feature extraction**, so there are few dependencies.

## Project structure

```
.
├── app.py                # Streamlit web app
├── features.py           # URL feature extraction + red-flag explanations
├── train.py              # Trains and compares models, saves model.joblib
├── make_sample_data.py   # Generates a synthetic demo dataset
├── sample_urls.csv       # Demo data (synthetic)
├── requirements.txt
└── README.md
```

## Getting started

**Requirements:** Python 3.9+

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. (Recommended) create a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model
python train.py sample_urls.csv

# 5. Launch the app
streamlit run app.py
```

The app opens at <http://localhost:8501>. If `streamlit` isn't recognised, use `python -m streamlit run app.py`.

## Using your own dataset

Provide a CSV with two columns, `url` and `label`:

```csv
url,label
https://www.wikipedia.org/,0
http://paypal-verify.example.xyz/login.php,1
```

Labels `0`, `benign` and `good` count as safe. Labels `1`, `malicious`, `phishing`, `bad`, `defacement`, `malware` and `unsafe` count as malicious. Then run:

```bash
python train.py path/to/your_data.csv
```

Suggested public sources: [PhishTank](https://phishtank.org/), and the "Malicious URLs dataset" on Kaggle.

## Batch scoring

In the **Batch** tab, upload a CSV with a `url` column. The app adds `risk` (0 to 1) and `verdict` columns, and you can download the results.

## Important limitations

- **The bundled model is trained on synthetic data.** The demo dataset is easy to separate, so its near-perfect accuracy is *not* representative. Retrain on real data before relying on any result.
- **URL-only analysis.** The model can't see page content, domain age, WHOIS, DNS or certificates, so it can miss sophisticated attacks and flag some legitimate URLs.
- This is an educational/portfolio project, **not** a replacement for a production security product. Treat its output as one signal among many.

## Ideas for improvement

- Train on a large real-world dataset and report precision/recall, not just accuracy
- Add domain-based features (WHOIS age, DNS records, SSL info)
- Try gradient boosting (XGBoost / LightGBM) or character-level n-gram models
- Add cross-validation and a confusion-matrix view in the UI
- Package as a REST API (FastAPI) or browser extension

## Tech stack

Python · scikit-learn · pandas · joblib · Streamlit

## License

Add a license of your choice (e.g. [MIT](https://choosealicense.com/licenses/mit/)) and describe it here.
