import pandas as pd
import numpy as np
import math

# Read the term weights from CSV
df = pd.read_csv('term_weights.csv', index_col=0)

# Extract the query weights
query_weights = df['Q']

# Calculate document similarities using Dice coefficient
dice_similarities = {}
for doc in ['D1', 'D2', 'D3']:
    # Calculate the dot product of query weights and document weights
    dot_product = sum(query_weights[i] * df[doc][i] for i in range(len(query_weights)))
    
    # Calculate the sum of squares for query weights
    query_sum_squares = sum(query_weights[i] ** 2 for i in range(len(query_weights)))
    
    # Calculate the sum of squares for document weights
    doc_sum_squares = sum(df[doc][i] ** 2 for i in range(len(query_weights)))
    
    # Calculate the Dice coefficient
    dice_coefficient = (2 * dot_product) / (query_sum_squares + doc_sum_squares)
    
    # Round to 3 decimal places
    dice_similarities[doc] = round(dice_coefficient, 3)

# Print the Dice similarities
print("Document Similarities (Dice Coefficient):")
for doc, sim in dice_similarities.items():
    print(f"{doc}: {sim}")

# Create a DataFrame for the similarities and sort by similarity value
df_similarities = pd.DataFrame(dice_similarities.items(), columns=["Document", "Dice Similarity"])
df_similarities = df_similarities.sort_values("Dice Similarity", ascending=False)

# Save the similarities to CSV
df_similarities.to_csv("dice_similarities.csv", index=False)
print("\nResults saved to dice_similarities.csv")