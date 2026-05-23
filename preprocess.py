# ---------------------
# PREPROCESSING MODULE
# ---------------------
# Covers Assignment Step 1:
# 1.1 Tokenization
# 1.2 Remove special characters & stop words
# 1.3 Return cleaned tweets

import re

def load_stopwords(path):
    """Load stopwords from a plain-text file (one word per line)."""
    with open(path, "r") as f:
        return set(word.strip() for word in f.readlines())

def clean_text(text, stopwords):
    """
    1.1  Tokenisation   – split on whitespace after normalisation
    1.2  Remove noise   – URLs, non-alpha chars, stopwords, short tokens
    1.3  Return string  – rejoin cleaned tokens
    """
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', ' ', text)   # strip URLs
    text = re.sub(r'[^a-z\s]', ' ', text)         # keep only letters

    tokens = text.split()                          # 1.1 tokenise
    tokens = [t for t in tokens                   # 1.2 filter
              if t not in stopwords and len(t) > 2]

    return " ".join(tokens)                        # 1.3 return

# ── Label mapping for the 3-class dataset ─────────────────────────────────
# LABEL_MAP = {
#     -1: "negative",
#      0: "neutral",
#      1: "positive"
# }
LABEL_MAP = {
      0: "negative",
      4: "positive"
 }