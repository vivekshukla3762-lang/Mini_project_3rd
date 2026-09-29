"""Interactive UI:  streamlit run app.py"""
import joblib, pandas as pd, streamlit as st
from features import extract_features, explain, FEATURE_NAMES

st.set_page_config(page_title="URL Threat Detector", page_icon="🛡️", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("model.joblib")

try:
    model = load_model()
except FileNotFoundError:
    st.error("model.joblib not found. Run:  python make_sample_data.py && python train.py sample_urls.csv")
    st.stop()

def score(url):
    x = pd.DataFrame([extract_features(url)])[FEATURE_NAMES]
    return float(model.predict_proba(x)[0][1]), x

st.title("🛡️ Malicious URL Detector")
st.caption("ML-based check using URL structure only. It never visits the link.")

tab1, tab2, tab3 = st.tabs(["Single URL", "Batch (CSV)", "Model info"])

with tab1:
    url = st.text_input("Enter a URL", placeholder="http://paypal-verify.example.xyz/login.php")
    if url:
        p, x = score(url)
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Risk score", f"{p*100:.1f}%")
            st.progress(min(max(p, 0.0), 1.0))
            if p >= 0.7: st.error("Likely malicious")
            elif p >= 0.4: st.warning("Suspicious")
            else: st.success("Likely safe")
        with c2:
            st.subheader("Red flags")
            flags = explain(url)
            for f in flags: st.write("⚠️ " + f)
            if not flags: st.write("No obvious red flags.")
        with st.expander("Extracted features"):
            st.dataframe(x.T.rename(columns={0: "value"}))
        if hasattr(model, "feature_importances_"):
            imp = pd.Series(model.feature_importances_, index=FEATURE_NAMES).sort_values(ascending=False).head(10)
            st.subheader("Top model features"); st.bar_chart(imp)

with tab2:
    up = st.file_uploader("CSV with a 'url' column", type="csv")
    if up:
        df = pd.read_csv(up)
        if "url" not in df.columns:
            st.error("CSV needs a 'url' column.")
        else:
            df["risk"] = [score(u)[0] for u in df["url"].astype(str)]
            df["verdict"] = pd.cut(df["risk"], [-1, .4, .7, 2], labels=["safe", "suspicious", "malicious"])
            st.dataframe(df.sort_values("risk", ascending=False), use_container_width=True)
            st.bar_chart(df["verdict"].value_counts())
            st.download_button("Download results", df.to_csv(index=False), "results.csv")

with tab3:
    st.write(f"**Model:** `{type(model).__name__ if not hasattr(model, 'steps') else model.steps[-1][1].__class__.__name__}`")
    st.write(f"**Features used:** {len(FEATURE_NAMES)}")
    st.write(", ".join(FEATURE_NAMES))
    st.info("The bundled model is trained on SYNTHETIC data. Retrain on a real dataset "
            "(PhishTank / Kaggle Malicious URLs) with `python train.py your_data.csv` for real use.")
