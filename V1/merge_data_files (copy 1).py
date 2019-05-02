import pandas as pd
import os.path
'''

df = pd.read_csv('/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/10days100repo-fork/2015-02-1.csv')
df=df.loc[df['2015-02-1']>0]
#dfList = df[]
files =[]
for i in range(0,9):
	for j in range(0,4):
			files.append('10days100repo-fork/2015-0%d-%d.csv' %(i,j))
#print(files)
for i in files:
	if os.path.isfile(i):
		print('%s is' %i)
		df2=pd.read_csv(i)
		df = pd.merge(df,df,on='name_h')

df.to_csv('merged_files.csv',index=False)
'''
import numpy as np
import matplotlib.pyplot as plt
Dir = '/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/10days100repo-fork/'
Fls = os.listdir(Dir)
Data = []
for _,f in enumerate(Fls):
	data = pd.read_csv(Dir + f)
	Data.append(data.ix[:,1].tolist())
Data = np.array(Data)
print(Data.shape)
f, ax = plt.subplots(10,sharex=True)
for i in range(10):
	ax[i].plot(Data[:,i])
plt.show()