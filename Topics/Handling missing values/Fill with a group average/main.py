import pandas as pd
df = pd.read_csv('./data/dataset/input.txt')

df["height"] = df.groupby("location")["height"].apply(lambda x: x.fillna(round(x.mean(), 1)))#.sum()
#print(df['height'][0]-1/10**20)
print(df)
