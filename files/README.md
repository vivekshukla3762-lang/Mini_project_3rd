# Malicious URL Detector

    pip install -r requirements.txt
    python make_sample_data.py          # synthetic demo data (skip if you have real data)
    python train.py sample_urls.csv     # trains LogReg + RandomForest, saves model.joblib
    streamlit run app.py                # interactive UI

Use real data: a CSV with columns `url,label` (PhishTank, Kaggle "Malicious URLs dataset", etc.).
