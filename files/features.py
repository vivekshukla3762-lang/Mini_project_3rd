"""URL feature extraction (stdlib only). Used by train.py, app.py and predict."""
import math, re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = ["login", "signin", "verify", "update", "secure", "account", "bank", "confirm",
                    "password", "paypal", "wallet", "billing", "suspend", "support", "free", "bonus", "claim"]
SHORTENERS = {"bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly", "cutt.ly", "rb.gy"}
RISKY_TLDS = {"xyz", "top", "tk", "ml", "ga", "cf", "gq", "click", "work", "zip", "country", "loan", "icu", "cam"}
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

FEATURE_NAMES = [
    "url_len", "host_len", "path_len", "query_len", "num_dots", "num_hyphens", "num_underscores",
    "num_digits", "digit_ratio", "num_special", "num_subdomains", "path_depth", "num_params",
    "has_ip", "has_at", "has_https", "has_port", "double_slash_in_path", "is_shortener",
    "risky_tld", "suspicious_words", "host_entropy", "url_entropy", "hex_encoded", "brand_in_subdomain",
]
BRANDS = ["paypal", "google", "apple", "microsoft", "amazon", "facebook", "netflix", "sbi", "hdfc", "icici"]


def _entropy(s):
    if not s:
        return 0.0
    n = len(s)
    return -sum((s.count(c) / n) * math.log2(s.count(c) / n) for c in set(s))


def parse(url):
    url = url.strip()
    p = urlparse(url if "://" in url else "http://" + url)
    return url, p, (p.hostname or "")


def extract_features(url):
    url, p, host = parse(url)
    labels = [l for l in host.split(".") if l]
    tld = labels[-1] if labels else ""
    low = url.lower()
    path = p.path or ""
    special = sum(not c.isalnum() for c in url)
    digits = sum(c.isdigit() for c in url)
    sub = labels[:-2]
    return {
        "url_len": len(url), "host_len": len(host), "path_len": len(path), "query_len": len(p.query),
        "num_dots": url.count("."), "num_hyphens": url.count("-"), "num_underscores": url.count("_"),
        "num_digits": digits, "digit_ratio": digits / max(len(url), 1), "num_special": special,
        "num_subdomains": max(len(labels) - 2, 0), "path_depth": path.count("/"),
        "num_params": len([q for q in p.query.split("&") if q]),
        "has_ip": int(bool(IP_RE.match(host))), "has_at": int("@" in url),
        "has_https": int(p.scheme == "https"), "has_port": int(_port(p) is not None),
        "double_slash_in_path": int("//" in path), "is_shortener": int(host in SHORTENERS),
        "risky_tld": int(tld in RISKY_TLDS),
        "suspicious_words": sum(w in low for w in SUSPICIOUS_WORDS),
        "host_entropy": _entropy(host), "url_entropy": _entropy(url),
        "hex_encoded": low.count("%"),
        "brand_in_subdomain": int(any(b in ".".join(sub) for b in BRANDS)),
    }


def _port(p):
    try:
        return p.port
    except ValueError:
        return -1


def explain(url):
    """Human-readable red flags for the UI."""
    f = extract_features(url)
    flags = []
    if f["has_ip"]: flags.append("Host is a raw IP address")
    if f["has_at"]: flags.append("Contains '@' (can hide the real destination)")
    if not f["has_https"]: flags.append("Not using HTTPS")
    if f["is_shortener"]: flags.append("Uses a URL shortener")
    if f["risky_tld"]: flags.append("Uses a TLD common in abuse")
    if f["suspicious_words"] >= 2: flags.append(f"{f['suspicious_words']} suspicious keywords (login, verify, ...)")
    if f["brand_in_subdomain"]: flags.append("Brand name used in a subdomain (possible impersonation)")
    if f["num_subdomains"] >= 3: flags.append("Many subdomains")
    if f["url_len"] > 75: flags.append("Very long URL")
    if f["num_hyphens"] >= 3: flags.append("Many hyphens")
    if f["hex_encoded"] >= 3: flags.append("Heavy percent-encoding")
    return flags
