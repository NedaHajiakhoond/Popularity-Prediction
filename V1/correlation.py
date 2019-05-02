import pandas as pd
import numpy as np
import os.path

np.random.seed(7)
Dir = '/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/10days166-100repos-watch/'
Fls = os.listdir(Dir)
Data = []
print(len(Fls))


for _,f in enumerate(Fls):
	data = pd.read_csv(Dir + f)
	#print(len(data))
	Data.append(data.ix[:,1].tolist())
Data = np.array(Data)
d = {'x1': [1, 4, 4, 5, 6],
     'x2': [0, 0, 8, 2, 4],
     'x3': [2, 8, 8, 10, 12],
     'x4': [-1, -4, -4, -4, -5]}
d={}
i = 0
for i in range(Data.shape[1]):
     d[i]=Data[:,i]
df = pd.DataFrame(data = d)
print("Data Frame")
print(df)
print()

print("Correlation Matrix")
print(df.corr())
print()

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=100):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

print("Top Absolute Correlations")
print(get_top_abs_correlations(df, 100))
