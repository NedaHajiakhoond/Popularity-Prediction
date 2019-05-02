import json
import pandas as pd
from pymongo import MongoClient
import urllib.parse
import ssl
import pandas as pd
import time
import gc
import os
import shutil
import pathlib
import itertools
class WeeklyData:
	
	def __init__(self):				
		user =urllib.parse.quote_plus("nbidoki")
		pw = urllib.parse.quote_plus("NBidokiS0cialS1m")
		uri = "mongodb://%s:%s@10.0.2.153:27017/?authMechanism=SCRAM-SHA-1" % (user, pw)
		client = MongoClient(uri,
							 ssl=True,
							 ssl_cert_reqs=ssl.CERT_NONE)
		print("Start")		
		#db_name = "top-1000-users"
		db_name = "github-training"
		self.db = client[db_name]
				

	def get_repo_creator(self,repo):
		query_start_time = time.time()
		query_results = self.db.Repository_Profile.find({"full_name_h": repo},{"full_name_h":1,"owner.login_h" : 1} )
		df = pd.DataFrame(list(query_results))
		df = pd.concat([df.drop(["owner"], axis=1), df["owner"].apply(pd.Series)], axis=1)
		#print(df)
		return df	
		
		
	def find_repo_creator(self,fl):
		repos = pd.read_csv(fl,nrows=100)
		repos_list=repos['name_h'].tolist()
		creators_df = pd.DataFrame(columns=['full_name_h','login_h'])
		for i,repo in enumerate(repos_list):
			#print(repo)
			df = self.get_repo_creator(repo)
			creators_df =creators_df.append(df)
		creators_df.to_csv('repos_creators.csv')
		creators_list = creators_df['login_h'].tolist()
		return creators_list

		

	def find_weekly_comp(self,creators_file):
		creators_df = pd.read_csv(creators_file)
		creators_list = creators_df['login_h'].tolist()
		creators_list=creators_list
		Dir = '/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/Weekly-WATCH/'
		Fls = os.listdir(Dir)
		Data = []
		for _,f in enumerate(Fls):
			print('week: %s'%f)
			m = f.split('.')
			data = []
			weekly_df = pd.DataFrame(columns=['login_h','%s'%f])
			with open('/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/Weekly-WATCH/%s'%f) as cf:
				for line in cf:
					l = json.loads(line)
					#data.append(json.loads(line))
					if (l["User ID"] in creators_list):
						#print(l["Measures"][0]["Measure"][1])
						weekly_df = weekly_df.append({'login_h': l["User ID"],'%s'%f : l["Measures"][0]["Measure"][1]}, ignore_index = True)
						
			weekly_df.to_csv('/home/social-sim/Desktop/SocialSimCodeTesting/Pop_MLearning/Weekly-WATCH-components/%s.csv'%m[0])		
			'''
			for i,creator in enumerate(creators_list):
				for d in data:
					if d[]
			'''
				
	