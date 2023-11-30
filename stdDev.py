import pandas as pd

data = pd.read_csv("HowManyEntries.csv")
print(data.mean(), data.std())