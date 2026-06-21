import pandas as pd
import joblib
import torch
from transformers import AutoTokenizer, AutoModel
import warnings
import os
import numpy as np

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

print("="*50)
print("Starting prediction script...")
print("="*50)

# -------------------------------
# Load model and label map
# -------------------------------
print("\n[1/5] Loading trained model...")
with open(r"C:\Users\aditya\Downloads\LR_DP_finetuned_BERT.pkl", 'rb') as f:
    model = joblib.load(f)
print("Model loaded successfully!")

print("\n[2/5] Loading label map...")
with open(r"C:\Users\aditya\Downloads\labels.pkl", 'rb') as f:
    label_map = joblib.load(f)
print(f"Label map loaded! Available labels: {list(label_map.values())}")

# Build a robust id -> label mapping regardless of how labels.pkl was stored
id_to_label = {}

# Case 1: label_map looks like {label_name: class_id}
if all(isinstance(v, (int, np.integer)) for v in label_map.values()):
    id_to_label = {int(v): k for k, v in label_map.items()}
# Case 2: label_map looks like {class_id: label_name} with mixed key types
else:
    for k, v in label_map.items():
        if isinstance(k, (int, np.integer)):
            id_to_label[int(k)] = v
        elif isinstance(k, str) and k.isdigit():
            id_to_label[int(k)] = v

print(f"Resolved class-id map entries: {len(id_to_label)}")

# -------------------------------
# Load Hugging Face BERT model and tokenizer
# -------------------------------
print("\n[3/5] Loading BERT model and tokenizer (this may take a moment)...")
bert_model_name = "necromancer7/BertDatav3Final"
tokenizer = AutoTokenizer.from_pretrained(bert_model_name)
bert_model = AutoModel.from_pretrained(bert_model_name)
print("BERT model and tokenizer loaded successfully!")

# -------------------------------
# Function to get BERT embedding in batches
# -------------------------------
def get_bert_embedding_batch(texts, batch_size=32):
    """Process texts in smaller batches to avoid memory issues"""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        print(f"  Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1} ({i+1}-{min(i+batch_size, len(texts))} of {len(texts)})")
        
        tokens = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        )
        
        with torch.no_grad():
            outputs = bert_model(**tokens)
        
        # Take mean of token embeddings
        batch_embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
        all_embeddings.append(batch_embeddings)
    
    # Combine all batches
    final_embeddings = np.vstack(all_embeddings)
    print(f"  All embeddings generated! Final shape: {final_embeddings.shape}")
    return final_embeddings

# -------------------------------
# Batch inference
# -------------------------------
print("\n[4/5] Loading your data file...")
# Load the split CSV file
df = pd.read_csv(r"C:\Users\aditya\Downloads\output_predictions - output_predictions.csv")
print(f"Data loaded! Total rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Check if the column is named "Text_Chunks" (from your split script)
if "text" in df.columns:
    text_column = "text"
elif "Pattern String" in df.columns:
    text_column = "Pattern String"
else:
    raise ValueError(f"CSV must have a 'text' or 'Pattern String' column. Found: {df.columns.tolist()}")

print(f"Using column: '{text_column}'")

# Clean text values so tokenizer always receives valid strings
raw_texts = df[text_column].tolist()
cleaned_texts = []
null_count = 0
non_string_count = 0

for value in raw_texts:
    if pd.isna(value):
        cleaned_texts.append("")
        null_count += 1
    elif isinstance(value, str):
        cleaned_texts.append(value)
    else:
        cleaned_texts.append(str(value))
        non_string_count += 1

if null_count or non_string_count:
    print(f"Cleaned text column values: {null_count} null -> empty string, {non_string_count} non-string -> string")

print(f"\nSample of first 3 rows:")
for i in range(min(3, len(df))):
    print(f"  Row {i+1}: {cleaned_texts[i][:100]}...")

# Get embeddings in batches
print(f"\n[5/5] Getting BERT embeddings and making predictions...")
print(f"Processing {len(df)} texts in batches of 32...")
embeddings = get_bert_embedding_batch(cleaned_texts, batch_size=32)

# Predict with the model
print("\nRunning predictions on all embeddings...")
predictions = model.predict(embeddings)
print("Predictions complete!")

# Map predictions to labels
print("Mapping predictions to labels...")
mapped_predictions = []
missing_ids = set()

for p in predictions:
    class_id = int(p)
    label = id_to_label.get(class_id)
    if label is None:
        missing_ids.add(class_id)
        label = f"UNKNOWN_{class_id}"
    mapped_predictions.append(label)

if missing_ids:
    print(f"Warning: Missing labels for class IDs: {sorted(missing_ids)}")

df["prediction"] = mapped_predictions

# Save results
output_path = r"C:\Users\aditya\Downloads\output_predictions.csv"
df[[text_column, "prediction"]].to_csv(output_path, index=False, encoding='utf-8-sig')

print("\n" + "="*50)
print("PREDICTION COMPLETE!")
print("="*50)
print(f"Total texts processed: {len(df)}")
print(f"Output saved to: {output_path}")
print(f"\nPrediction distribution:")
print(df["prediction"].value_counts())
print("="*50)