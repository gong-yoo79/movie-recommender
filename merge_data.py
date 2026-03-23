import pandas as pd

# Load both datasets
df1 = pd.read_csv("small_movies.csv")
df2 = pd.read_csv("bollywood_movies.csv")

# Keep only required columns (important)
df1 = df1[['title', 'overview', 'genres']]
df2 = df2[['title', 'overview', 'genres']]

# Combine datasets
final_df = pd.concat([df1, df2], ignore_index=True)

# Save new dataset
final_df.to_csv("final_movies.csv", index=False)

print("✅ Combined dataset created!")
