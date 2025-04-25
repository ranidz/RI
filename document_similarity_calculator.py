import pandas as pd
import numpy as np
import math

# Read the term weights from CSV
df = pd.read_csv('term_weights.csv', index_col=0)

# Extract the query weights
query_weights = df['Q']

# Calculate document similarities
similarities = {}
for doc in ['D1', 'D2', 'D3']:
    # Calculate the dot product of query weights and document weights
    similarity = sum(query_weights[i] * df[doc][i] for i in range(len(query_weights)))
    similarities[doc] = round(similarity, 3)

# Print the similarities
print("Document Similarities (RSV):")
for doc, sim in similarities.items():
    print(f"{doc}: {sim}")

# Create a DataFrame for the similarities and sort by similarity value
df_similarities = pd.DataFrame(similarities.items(), columns=["Document", "Similarity"])
df_similarities = df_similarities.sort_values("Similarity", ascending=False)

# Save the similarities to CSV
df_similarities.to_csv("document_similarities.csv", index=False)
print("\nResults saved to document_similarities.csv")