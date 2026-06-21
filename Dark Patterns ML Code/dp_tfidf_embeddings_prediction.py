import pandas as pd
import pickle

# Load model and label map
with open("logreg_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

with open("labels.pkl", "rb") as f:
    label_map = pickle.load(f)

# Load CSV
df = pd.read_csv("cleaned.csv")

# Ensure 'text' column exists
if 'text' not in df.columns:
    raise ValueError("CSV must have a 'text' column")

# Predict
predictions = model.predict(df['text'])

# Map predictions to labels
df['prediction'] = [label_map[p] for p in predictions]

# Save to new CSV
df[['text', 'prediction']].to_csv("output.csv", index=False)

print("Predictions saved to output.csv")
