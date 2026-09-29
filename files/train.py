"""Usage: python train.py data.csv   (CSV needs columns: url,label  -> label: 0/benign/good, 1/malicious/phishing/bad)"""
import sys, joblib, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from features import extract_features, FEATURE_NAMES

path = sys.argv[1] if len(sys.argv) > 1 else "sample_urls.csv"
df = pd.read_csv(path).dropna(subset=["url", "label"]).drop_duplicates("url")
bad = {"1", "malicious", "phishing", "bad", "defacement", "malware", "unsafe"}
df["y"] = df["label"].astype(str).str.lower().isin(bad).astype(int)

X = pd.DataFrame([extract_features(u) for u in df["url"]])[FEATURE_NAMES]
X_tr, X_te, y_tr, y_te = train_test_split(X, df["y"], test_size=0.2, stratify=df["y"], random_state=42)

models = {
    "LogisticRegression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced"),
}
best, best_acc = None, -1
for name, m in models.items():
    m.fit(X_tr, y_tr)
    pred = m.predict(X_te)
    acc = accuracy_score(y_te, pred)
    print(f"\n=== {name} (accuracy {acc:.3f}) ===")
    print(classification_report(y_te, pred, target_names=["safe", "unsafe"], zero_division=0))
    if acc > best_acc: best, best_acc, best_name = m, acc, name

joblib.dump(best, "model.joblib")
print(f"Saved best model: {best_name}")
