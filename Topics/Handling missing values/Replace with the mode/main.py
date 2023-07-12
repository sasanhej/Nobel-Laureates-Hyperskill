#  write your code here 
import pandas as pd
df=pd.read_csv('./data/dataset/input.txt')
loc=df['location'].mode()[0]
df['location'].fillna(loc,inplace=True)
print(df.head(5))
