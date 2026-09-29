"""Generates a SYNTHETIC sample_urls.csv so the pipeline runs end-to-end.
Replace with a real dataset (e.g. Kaggle 'Malicious URLs dataset' / PhishTank) for real use."""
import random, string, pandas as pd
random.seed(42)
good_domains = ["google.com","wikipedia.org","github.com","stackoverflow.com","amazon.in","flipkart.com","bbc.co.uk",
  "nytimes.com","youtube.com","linkedin.com","microsoft.com","apple.com","python.org","medium.com","reddit.com",
  "hdfcbank.com","sbi.co.in","irctc.co.in","zomato.com","swiggy.com","coursera.org","nasa.gov","mit.edu","who.int"]
good_paths = ["", "/", "/about", "/products/item-{n}", "/docs/getting-started", "/blog/2024/{w}", "/search?q={w}",
  "/watch?v={r}", "/wiki/{w}", "/user/{w}/profile", "/category/{w}/page/{n}", "/help/contact"]
words = ["python","travel","music","science","news","sports","recipes","laptop","health","history","finance","games"]
brands = ["paypal","google","apple","microsoft","amazon","netflix","sbi","hdfc","icici","facebook"]
bad_tlds = ["xyz","top","tk","ml","ga","cf","click","work","icu","cam","zip"]
kw = ["login","verify","secure","update","account","confirm","signin","billing","wallet","support"]
rnd = lambda k: "".join(random.choices(string.ascii_lowercase + string.digits, k=k))
def good():
    u = random.choice(["https://","https://","https://www.","http://"]) + random.choice(good_domains)
    return u + random.choice(good_paths).format(n=random.randint(1,999), w=random.choice(words), r=rnd(11))
def bad():
    b, k, t = random.choice(brands), random.choice(kw), random.choice(bad_tlds)
    kind = random.randint(0, 5)
    if kind == 0: return f"http://{b}-{k}.{rnd(random.randint(5,10))}.{t}/{k}/{rnd(8)}.php"
    if kind == 1: return f"http://{random.randint(11,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}/{b}/{k}.html"
    if kind == 2: return f"http://{b}.{k}.{rnd(6)}.{random.choice(good_domains)[:-4]}-{rnd(4)}.{t}/index.php?user={rnd(6)}&token={rnd(20)}"
    if kind == 3: return f"https://{random.choice(good_domains)}@{rnd(9)}.{t}/{k}"
    if kind == 4: return f"http://{b}{k}{random.randint(1,99)}.{t}/wp-content/{rnd(6)}/{k}%2F{rnd(5)}%3D{rnd(4)}"
    return f"http://bit.ly/{rnd(7)}" if random.random() < .5 else f"http://{k}-{b}-{rnd(5)}.{t}:8080/{rnd(12)}"
rows = [(good(), 0) for _ in range(1500)] + [(bad(), 1) for _ in range(1500)]
pd.DataFrame(rows, columns=["url","label"]).sample(frac=1, random_state=1).to_csv("sample_urls.csv", index=False)
print("wrote sample_urls.csv", len(rows))
