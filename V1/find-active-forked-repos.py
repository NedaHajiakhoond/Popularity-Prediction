import pandas as pd
import os.path

df = pd.read_csv('/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/Months/2015-02.csv', nrows=500)
df=df.loc[df['2015-02']>1]
df = df.sort_values(['2015-02'],ascending=False)
df.to_csv('active_forked_repos_list.csv',index_label=False)
repo_list = df['name_h'].tolist()
print(len(repo_list))
