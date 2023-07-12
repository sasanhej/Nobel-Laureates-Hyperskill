import pandas as pd
import os
import requests
import sys
import string
import numpy as np
import datetime
import matplotlib.pyplot as plt

"""
if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")
"""

nb=pd.read_json('../Data/Nobel_laureates.json')
nb.to_csv('../Data/Nobel_laureateso.csv')

nb.dropna(subset='gender', axis=0, inplace=True)
nb.reset_index(inplace=True, drop=True)
newbi = nb['place_of_birth'].apply(lambda x: str.split(x, ",")[-1].strip() if (x is not None and ',' in x) else None)
nb['born_in'].replace(to_replace="", regex=True, value=np.nan, inplace=True)
nb['born_in'].fillna(newbi, inplace=True,axis=0)
nb['born_in'].replace(to_replace=['United States', 'U.S.', 'US'], regex=True, value='USA', inplace=True)
nb['born_in'].replace(to_replace=['USAA'], regex=True, value='USA', inplace=True)
nb['born_in'].replace(to_replace=['United Kingdom'], regex=True, value='UK', inplace=True)
nb.dropna(inplace=True, subset=["born_in"])
nb.reset_index(inplace=True, drop=True)
x=0
yy=list([])
for i in range(nb.shape[0]):
    x=nb.loc[i,'date_of_birth']
    if '-' in x:
        by=x[:4]
    else:
        by=x[-4:]
    yy.append(int(by))
nb['year_born']=yy
nb['age_of_winning']=nb.year-yy

cp=list([])
for i in range(nb.shape[0]):
    x=nb.loc[i,'born_in']
    if nb.value_counts("born_in")[x] < 25:
        x='Other countries'
    cp.append(x)
nb['ctpie']=cp

'''
pdata = nb.value_counts("ctpie").tolist()
plabels = nb.value_counts("ctpie").keys().tolist()
pcolors=['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
pexplode=[0,0,0,0.08,0.08,0.08,0.08,0.08,0.08]

plt.figure(figsize=(12, 12))
plt.pie(pdata,
        explode=pexplode,
        labels=plabels,
        colors=pcolors,
        autopct=lambda p:f'{p:.2f}%\n{p*sum(pdata)/100 :.0f}'
        )
plt.show()
'''

nb=nb[nb['category']!=""]
bm=(nb[nb['gender']=='male'].groupby(['category'])['category'].count())
bf=(nb[nb['gender']=='female'].groupby(['category'])['category'].count())
bmd=bm.tolist()
bfd=bf.tolist()
cat=bm.keys().tolist()
'''
x_axis = np.arange(len(cat))

plt.figure(figsize=(10, 10))

plt.bar(x_axis - 0.2, bmd, width=0.4, label='Males', color='blue')
plt.bar(x_axis + 0.2, bfd, width=0.4, label='Females', color='crimson')

# set tick labels and their location
plt.xticks(x_axis, cat)

plt.xlabel('Category', fontsize=14)
plt.ylabel('Nobel Laureates Count', fontsize=14)
plt.title('The total count of male and female Nobel Prize winners by categories', fontsize=20)

# add legend
plt.legend()

plt.show()
'''

Chemistry=nb[nb['category']=='Chemistry']['age_of_winning']
Economics=nb[nb['category']=='Economics']['age_of_winning']
Literature=nb[nb['category']=='Literature']['age_of_winning']
Peace=nb[nb['category']=='Peace']['age_of_winning']
Physics=nb[nb['category']=='Physics']['age_of_winning']
Physiology_or_Medicine=nb[nb['category']=='Physiology or Medicine']['age_of_winning']
All_categories=nb['age_of_winning']

data=[Chemistry,Economics,Literature,Peace,Physics,Physiology_or_Medicine,All_categories]

plt.figure(figsize=(10, 10))

labels = ['Chemistry','Economics','Literature','Peace','Physics','Physiology or Medicine','All categories']
plt.boxplot(data, labels=labels, showmeans=True)

plt.ylabel('Age of Obtaining the Nobel Prize', fontsize=14)
plt.xlabel('Category', fontsize=14)
plt.title('Distribution of Ages by Category', fontsize=20)

plt.show()