import pandas as pd
import joblib
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("dataset.csv")

pipe = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    LogisticRegression(C=10, class_weight="balanced", max_iter=1000)
)
pipe.fit(df["text"], df["intent"])

joblib.dump(pipe, "intent_model.pkl")
print("Saved. Classes:", list(pipe.classes_))