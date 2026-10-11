import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict

df = pd.read_csv("dataset.csv")

pipe = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000)
)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(pipe, df["text"], df["intent"], cv=cv)
print("Fold scores:", scores.round(2))
print(f"Mean: {scores.mean():.3f}  Std: {scores.std():.3f}")

pred = cross_val_predict(pipe, df["text"], df["intent"], cv=cv)
print("\nMisclassified across all folds:")
for text, true, guess in zip(df["text"], df["intent"], pred):
    if true != guess:
        print(f"  '{text}'  true={true}  predicted={guess}")

for C in [1, 10, 100]:
    pipe = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)),
        LogisticRegression(C=C, max_iter=1000)
    )
    s = cross_val_score(pipe, df["text"], df["intent"], cv=cv)
    print(f"C={C}: mean={s.mean():.3f}")