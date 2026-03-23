import pandas as pd

# load original dataset
df = pd.read_csv("tmdb_5000_movies.csv")

# reduce size (only 500 rows)
df = df.head(500)

# save new smaller dataset
df.to_csv("small_movies.csv", index=False)

print("✅ Small dataset created!")
