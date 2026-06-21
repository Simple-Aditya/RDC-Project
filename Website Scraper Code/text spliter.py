import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
print("Starting the script...")

print("Reading CSV file...")
file_path = r"" # fill in the path to your CSV file
df = pd.read_csv(file_path, encoding='utf-8')
print(f"CSV file loaded successfully! Total rows: {len(df)}")
print(f"Columns in the dataframe: {df.columns.tolist()}")

print("\nExtracting 'Text' column...")
text_column = df.iloc[:, 2]  # Third column (index 2)
print(f"Total text entries found: {len(text_column)}")

# Step 3: Split text into chunks of 5-6 words (preserving symbols)
print("\nSplitting text into 5-6 word chunks (preserving all symbols)...")
all_chunks = []
row_counter = 0

for idx, text in enumerate(text_column):
    if pd.notna(text):
        row_counter += 1
        print(f"Processing row {row_counter}/{len(text_column)}...")
        
        # Convert to string
        text_str = str(text)
        
        # Split by whitespace while preserving all symbols
        words = text_str.split()
        
        print(f"  Total words/tokens in this row: {len(words)}")
        
        # Create chunks of 5-6 words
        chunk_count = 0
        i = 0
        while i < len(words):
            # Alternate between 5 and 6 words per chunk
            chunk_size = 5 if (i // 5) % 2 == 0 else 6
            chunk = ' '.join(words[i:i+chunk_size])
            all_chunks.append(chunk)
            chunk_count += 1
            i += chunk_size
        
        print(f"  Created {chunk_count} chunks from this row")
    else:
        print(f"Skipping row {idx+1} - No text found")

print(f"\nTotal chunks created: {len(all_chunks)}")

# Step 4: Create new dataframe with split data
print("\nCreating new dataframe...")
new_df = pd.DataFrame(all_chunks, columns=['Text_Chunks'])
print(f"New dataframe created with {len(new_df)} rows")

# Step 5: Save to CSV
print("\nSaving to CSV...")
output_path = r"" # fill in the path where you want to save the split data
new_df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"CSV file saved successfully at: {output_path}")

print("\n=== SCRIPT COMPLETED SUCCESSFULLY ===")
print(f"Total chunks saved: {len(new_df)}")
print("Open the CSV file to see all the data with preserved symbols!")